# DeliverEase — Premium Logistics & Resource Management System

DeliverEase is a robust, production-ready, and beautifully designed web application for real-time logistics routing, weather-adapted travel time predictions, and automated driver and fleet allocation. 

The production-ready, refactored, and thoroughly tested source code is located in the **[clean_version/](file:///Users/bhovaretanishq/Documents/logistics_project/clean_version)** directory. It runs flawlessly on PostgreSQL and features a state-of-the-art dispatch and fleet management flow.

---

## Key Features

- **Smart Geocoding & Route Calculation**: Uses `geopy` and the OpenStreetMap Nominatim service to locate coordinates for any origin/destination city in India without requiring paid API keys.
- **Dynamic Weather & Traffic Adaptations**: Integrates real-time weather alerts via the Open-Meteo API. Automatically applies calculated traffic and weather delay factors to estimate precise travel times.
- **Automated Double-Booking Prevention**: Dynamically queries PostgreSQL to fetch only currently available drivers and trucks. On assignment, resource states are immediately flipped to unavailable.
- **Real-time Active Dashboard**: Displays active deliveries with live status badges.
- **Premium Custom Confirmation Dialogs**: Custom-built HTML/CSS confirmation modals and success toast banners replace intrusive, blocking native browser alerts for a sleek user experience.
- **Auto-Release Resource Cycle**: Completing a delivery automatically marks the associated driver and truck as available again for the next dispatch cycle.

---

## Repository Architecture

The repository is structured as follows:

- **`clean_version/`** - The primary, fully working isolated project workspace.
  - `backend/` - High-performance Flask server, database pooled configuration, and API routes.
  - `data/` - Static CSV seed files for trucks and drivers.
  - `frontend/` - Modern dispatcher interface files powered by Tailwind CSS.
  - `requirements.txt` - Fixed and verified Python production dependencies.
  - `.gitignore` - Production rules keeping virtual environments and credentials secure and private.
  - `README.md` - Technical setup guide for local development.

---

## Quick Start (Local Setup)

Follow these step-by-step instructions to get DeliverEase running locally on your machine.

### Prerequisites
- Python 3.10+
- PostgreSQL (Homebrew or EnterpriseDB)

### 1. Navigate to the Clean Version Workspace
Open your terminal and enter the clean isolated workspace:
```bash
cd clean_version
```

### 2. Initialize Private Local Database
To make setting up completely painless without password prompts or system database configurations, you can run a private PostgreSQL server directly in the project directory:

Start PostgreSQL on port `5432`:

```bash
pg_ctl -D db_data -o "-p 5432" -l db_data/server.log start
```

### 3. Create the Project Database

Create a database named `logistics_db`:

```bash
createdb -p 5432 -U your_postgres_user logistics_db
```

### 4. Connect to the Database

You can connect to the database using:

```bash
psql -p 5432 -U your_postgres_user -d logistics_db

### 3. Configure Environment Variables
Create a file named `.env` inside the `backend/` directory and paste the following parameters:

```env
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432
```

### 4. Setup Virtual Environment & Install Dependencies
Activate a Python virtual environment inside the clean folder:

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install all required production libraries
pip install -r requirements.txt
```

### 5. Create Tables & Seed Data
Run the database migration script. This will connect to your PostgreSQL instance, configure the relational schemas (`drivers`, `trucks`, `deliveries`), and seed them using files in the `data/` directory:

```bash
python backend/setup_db.py
```

### 6. Launch the Server
Start the Flask backend API:

```bash
python backend/app.py
```
The server will boot up and listen for requests at `http://127.0.0.1:5000`.

### 7. Run the Frontend
Simply double-click or open `frontend/index.html` in any web browser of your choice to launch the gorgeous dispatcher user interface!

---

##  API Endpoints Reference

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `POST /get_routes` | `POST` | Takes `{origin, destination}`. Returns weather-adapted time and distance. |
| `GET /get_available_resources` | `GET` | Returns list of all currently available drivers and trucks. |
| `POST /assign_delivery` | `POST` | Registers a delivery and flags the assigned driver & truck as unavailable. |
| `POST /confirm_delivery` | `POST` | Marks delivery as completed and frees up the driver and truck. |
| `GET /all_deliveries` | `GET` | Returns list of all active and completed deliveries in the system. |
| `GET /order_summary/<id>` | `GET` | Retrieves receipt-style details of a specific delivery by its ID. |

---

##  Deployment (Free on Render.com)

DeliverEase is fully prepared for instant production hosting on Render:
1. **Database**: Spin up a Free PostgreSQL Database on Render. Copy its *External Database URL*.
2. **Backend**: Deploy a Free Web Service. Connect your GitHub repository, set root directory to `clean_version`, set start command to `gunicorn --chdir backend app:app`, and add an environment variable `DATABASE_URL` with your Render database connection string.
3. **Frontend**: Update frontend `fetch` links to point to the live Render backend URL, commit, and deploy a Free Static Site pointing to the `clean_version/frontend` directory.
