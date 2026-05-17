from flask import Flask, request, jsonify
from flask_cors import CORS
from database import init_db
from routes import routes_bp

# Initialize Flask app, specifying the folder for static files
app = Flask(__name__, static_folder='frontend')

CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for frontend integration
app.register_blueprint(routes_bp)

@app.route("/")
def home():
    return "🚚 Logistics Management System Backend is Running"

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
