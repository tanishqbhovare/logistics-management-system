# DeliverEase — Logistics Management System

DeliverEase is a full-stack logistics management web application designed to manage delivery bookings, route planning, truck-driver assignment, pricing, and delivery tracking. The system helps users enter origin and destination locations, view route and distance details, select available drivers and trucks, provide client information, choose pricing plans, and confirm delivery assignments through a structured workflow.

The project is built using a Flask backend, PostgreSQL database, HTML/CSS/JavaScript frontend, and route prediction logic. It is designed as a clean academic/full-stack project demonstrating backend APIs, database operations, delivery management, and basic AI/ML-based route time prediction.

---

## Features

- Origin and destination input for delivery route planning
- Route distance and estimated travel time calculation
- Driver and truck availability management
- Truck and driver assignment workflow
- Client details collection
- Package weight-based pricing plans
- Delivery order summary page
- Delivery assignment confirmation
- Delivery status tracking
- PostgreSQL database integration
- Modular Flask backend structure
- Environment-variable based configuration
- Clean frontend flow for booking and assignment

---

## Tech Stack

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- Flask

### Database
- PostgreSQL

### Machine Learning / Prediction
- Python-based route time prediction logic
- Scikit-learn compatible structure for future model improvement

---

## Project Structure

```text
logistics-management-system/
│
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── routes.py
│   ├── setup_db.py
│   ├── route_prediction.py
│   ├── traffic_data.py
│   ├── weather_data.py
│   ├── utils.py
│   └── .env.example
│
├── frontend/
│   ├── index.html
│   ├── routes.html
│   ├── assigndelivery.html
│   ├── ordersummary.html
│   ├── final.html
│   ├── style.css
│   └── script.js
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Backend Setup

### 1. Clone the Repository

```bash
git clone https://github.com/tanishqbhovare/logistics-management-system.git
cd logistics-management-system
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

For Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Database Setup

This project uses PostgreSQL as the database.

### 1. Initialize a Local PostgreSQL Database Cluster

Create a local database cluster folder:

```bash
initdb -D db_data -U your_postgres_user --auth=scram-sha-256
```

Replace `your_postgres_user` with your PostgreSQL username.

### 2. Start PostgreSQL Server

Start PostgreSQL on port `5433`:

```bash
pg_ctl -D db_data -o "-p 5433" -l db_data/server.log start
```

### 3. Create the Project Database

```bash
createdb -p 5433 -U your_postgres_user logistics_db
```

### 4. Connect to the Database

```bash
psql -p 5433 -U your_postgres_user -d logistics_db
```

---

## Environment Variables

Create a `.env` file inside the `backend/` directory:

```bash
touch backend/.env
```

Add the following variables:

```env
DB_NAME=logistics_db
DB_USER=your_postgres_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5433
```

Do not commit your real `.env` file to GitHub.

Instead, keep a sample file named `.env.example`:

```env
DB_NAME=logistics_db
DB_USER=your_postgres_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5433
```

---

## Git Ignore Safety

The following files and folders should not be committed:

```gitignore
.env
*.env
backend/.env
db_data/
backend/db_data/
*.log
__pycache__/
venv/
.venv/
.DS_Store
```

---

## Run the Backend

Go to the backend folder:

```bash
cd backend
```

Run the Flask application:

```bash
python app.py
```

The backend will start locally, usually at:

```text
http://127.0.0.1:5000
```

---

## Frontend Flow

The application follows this delivery booking flow:

```text
index.html → routes.html → assigndelivery.html → ordersummary.html → final.html
```

### Flow Explanation

1. User enters origin and destination.
2. System calculates route details and distance.
3. User selects an available truck and driver.
4. User enters client details.
5. System displays order summary and pricing plans.
6. User confirms assignment.
7. Delivery is marked as assigned.

---

## Pricing Plans

| Package Weight | Price |
|---|---:|
| Less than 3 kg | ₹70 |
| 3 kg - 5 kg | ₹110 |
| 5 kg - 10 kg | ₹340 |
| 10 kg - 15 kg | ₹700 |

---

## Database Tables

The project uses the following main tables:

### trucks

Stores truck details and availability.

### drivers

Stores driver details and availability.

### deliveries

Stores delivery records, route details, assigned truck/driver, status, and timestamps.

---

## Security Notes

- Do not upload `.env` files to GitHub.
- Do not upload `db_data/` PostgreSQL folders.
- Do not expose real database passwords in README files.
- Use placeholder values in documentation.
- Use environment variables for sensitive configuration.

---

## Future Improvements

- Real-time MapmyIndia route and traffic integration
- Live delivery tracking
- Admin dashboard
- Driver dashboard
- Better machine learning model for delay prediction
- Authentication and role-based access
- Deployment on Render or Railway
- API documentation

---

## Author

Tanishq Bhovare

---

## Repository

```text
https://github.com/tanishqbhovare/logistics-management-system
```
