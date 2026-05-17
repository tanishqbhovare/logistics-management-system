from flask import Blueprint, request, jsonify
from database import get_connection
from route_prediction import predict_travel_time
import requests
import os
from dotenv import load_dotenv
from flask_cors import cross_origin
from traffic_data import get_traffic_data
from weather_data import get_weather_factor
import datetime
import os
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()


load_dotenv()
routes_bp = Blueprint("routes", __name__)
MAPMYINDIA_API_KEY = os.getenv("MAPMYINDIA_API_KEY")

# ---------------- Geocoding (Location to Coordinates) ----------------
from geopy.geocoders import Nominatim

def get_coordinates(city_name):
    try:
        geolocator = Nominatim(user_agent="logistics_project_clean")
        location = geolocator.geocode(city_name + ", India")
        if location:
            return location.latitude, location.longitude
    except Exception as e:
        print("Geocoding error:", e)
    return None, None

# ------------------ Route Suggestion ------------------
@routes_bp.route('/get_routes', methods=['POST'])
def get_routes():
    print("loc")
    data = request.json
    origin = data.get('origin')
    destination = data.get('destination')

    lat1, lon1 = get_coordinates(origin)
    lat2, lon2 = get_coordinates(destination)
    print(lat1,lon1,lat2,lon2)
    if not lat1 or not lat2:

        return jsonify({"error": "Invalid origin or destination"}), 400

    base_time,distance_km,traffic_factor = get_traffic_data(origin,destination)
    print("traffic factor",traffic_factor)
    weather_factor = get_weather_factor(lat2, lon2)
    print("weather factor",weather_factor)

    adjusted_time = round(base_time * traffic_factor * weather_factor, 2)
    return jsonify({
        "origin": origin,
        "destination": destination,
        "predicted_time_min": adjusted_time,
        "distance_km": distance_km,
        "traffic_factor": traffic_factor,
        "weather_factor": weather_factor
    })

# ------------------ Fetch Drivers & Trucks ------------------
@routes_bp.route('/get_available_resources', methods=['GET'])
@cross_origin(origins="*") 
def get_available_resources():
    conn = get_connection()
    cur = conn.cursor()

    # Drivers
    cur.execute("SELECT id, name, phone, is_available FROM drivers WHERE is_available = TRUE")
    drivers = cur.fetchall()

    # Trucks
    cur.execute("SELECT id, truck_number, fuel_efficiency, is_available FROM trucks WHERE is_available = TRUE")
    trucks = cur.fetchall()

    cur.close()
    conn.close()

    print("Drivers:", drivers)
    print("Trucks:", trucks)

    return jsonify({
        "drivers": drivers,
        "trucks": trucks
    })

# ------------------ Assign Delivery ------------------
@routes_bp.route('/assign_delivery', methods=['POST'])
def assign_delivery():
    data = request.json
    origin             = data.get("origin")
    destination        = data.get("destination")
    distance_km        = data.get("distance")
    predicted_time_min = data.get("travel_time")
    driver_id          = data.get("driver_id")
    truck_id           = data.get("truck_id")

    print("📦 Received Data:")
    print("Origin:", origin)
    print("Destination:", destination)
    print("Distance:", distance_km)
    print("Travel Time:", predicted_time_min)
    print("Driver ID:", driver_id)
    print("Truck ID:", truck_id)

    if not all([origin, destination, distance_km, predicted_time_min, driver_id, truck_id]):
        return jsonify({"error": "Missing required delivery data"}), 400

    # ... (rest of the function)


    conn = get_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()

    try:
        # Insert into deliveries and return the delivery ID
        cur.execute("""
            INSERT INTO deliveries (
                origin, destination, distance_km, predicted_time_min,
                truck_id, driver_id, status, delivery_start
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            origin, destination, distance_km, predicted_time_min,
            truck_id, driver_id, "Assigned", datetime.datetime.now()
        ))

        row = cur.fetchone()
        if not row:
            conn.rollback()
            cur.close()
            conn.close()
            return jsonify({"error": "Failed to assign delivery"}), 500

        delivery_id = row["id"]

        # Mark the driver and truck as unavailable
        cur.execute("UPDATE drivers SET is_available = FALSE WHERE id = %s", (driver_id,))
        cur.execute("UPDATE trucks  SET is_available = FALSE WHERE id = %s", (truck_id,))

        conn.commit()
        return jsonify({
            "message": "Delivery assigned successfully.",
            "delivery_id": delivery_id
        }), 201

    except Exception as e:
        conn.rollback()
        print("Assignment Error:", e)
        return jsonify({"error": "Internal server error during assignment"}), 500

    finally:
        cur.close()
        conn.close()




# ------------------ Confirm Delivery ------------------
@routes_bp.route('/confirm_delivery', methods=['POST'])
def confirm_delivery():
    try:
        data = request.json
        delivery_id = data.get("delivery_id")

        if not delivery_id:
            return jsonify({"error": "Delivery ID is required"}), 400

        conn = get_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cur = conn.cursor()

        # Get driver and truck assigned to the delivery
        cur.execute("SELECT driver_id, truck_id FROM deliveries WHERE id = %s", (delivery_id,))
        result = cur.fetchone()

        if not result:
            return jsonify({"error": "Delivery not found"}), 404

        driver_id = result['driver_id']
        truck_id = result['truck_id']

        # Update delivery status and mark as complete
        cur.execute("""
            UPDATE deliveries 
            SET status = %s, delivery_end = %s 
            WHERE id = %s
        """, ("Completed", datetime.datetime.now(), delivery_id))

        # Make truck & driver available again
        cur.execute("UPDATE drivers SET is_available = TRUE WHERE id = %s", (driver_id,))
        cur.execute("UPDATE trucks SET is_available = TRUE WHERE id = %s", (truck_id,))

        conn.commit()
        return jsonify({"message": "Delivery marked as complete and resources freed."})

    except Exception as e:
        print("Error confirming delivery:", e)
        if conn:
            conn.rollback()
        return jsonify({"error": "Failed to confirm delivery"}), 500
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()


@routes_bp.route('/order_summary/<int:delivery_id>', methods=['GET'])
def order_summary(delivery_id):
    """
    Retrieve a summary of the order based on delivery_id.
    Returns all details and a confirmation message.
    """
    conn = get_connection()
    cur = conn.cursor()
    
    # Get all delivery details
    cur.execute("""
        SELECT d.id, d.origin, d.destination, d.distance_km, d.predicted_time_min, 
               d.status, d.delivery_start, d.delivery_end,
               dr.id as driver_id, dr.name as driver_name, dr.phone as driver_phone,
               t.id as truck_id, t.truck_number
        FROM deliveries d
        JOIN drivers dr ON d.driver_id = dr.id
        JOIN trucks t ON d.truck_id = t.id
        WHERE d.id = %s
    """, (delivery_id,))
    
    result = cur.fetchone()
    
    if not result:
        return jsonify({"error": "Delivery not found"}), 404
    
    # Access the data using column names instead of numeric indices
    delivery_start = result['delivery_start'].strftime("%Y-%m-%d %H:%M:%S") if result['delivery_start'] else None
    delivery_end = result['delivery_end'].strftime("%Y-%m-%d %H:%M:%S") if result['delivery_end'] else None
    
    # Create response
    summary = {
        "delivery_id": result['id'],
        "origin": result['origin'],
        "destination": result['destination'],
        "distance_km": result['distance_km'],
        "estimated_time_min": result['predicted_time_min'],
        "status": result['status'],
        "delivery_start": delivery_start,
        "delivery_end": delivery_end,
        "driver": {
            "id": result['driver_id'],
            "name": result['driver_name'],
            "phone": result['driver_phone']
        },
        "truck": {
            "id": result['truck_id'],
            "truck_number": result['truck_number']
        },
        "message": "Your order is confirmed and has been assigned for delivery."
    }
    
    conn.close()
    
    return jsonify(summary)


# You can also create a route to get all orders/deliveries
@routes_bp.route('/all_deliveries', methods=['GET'])
def all_deliveries():
    """
    Retrieve a list of all deliveries in the system.
    """
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT d.id, d.origin, d.destination, d.status, d.delivery_start,
                   dr.name as driver_name, t.truck_number
            FROM deliveries d
            JOIN drivers dr ON d.driver_id = dr.id
            JOIN trucks t ON d.truck_id = t.id
            ORDER BY d.delivery_start DESC
        """)
        
        deliveries = cur.fetchall()
        
        result = []
        for delivery in deliveries:
            delivery_start = delivery['delivery_start'].strftime("%Y-%m-%d %H:%M:%S") if delivery['delivery_start'] else None
            
            result.append({
                "delivery_id": delivery['id'],
                "origin": delivery['origin'],
                "destination": delivery['destination'],
                "status": delivery['status'],
                "delivery_start": delivery_start,
                "driver_name": delivery['driver_name'],
                "truck_number": delivery['truck_number']
            })
        
        return jsonify({"deliveries": result})
    except Exception as e:
        print("Error fetching deliveries:", e)
        return jsonify({"error": "Failed to fetch deliveries"}), 500
    finally:
        cur.close()
        conn.close()