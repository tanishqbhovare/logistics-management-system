import csv
import os
from database import init_db, get_connection

# 1. Initialize tables
init_db()

# 2. Paths to CSV files
BASE = os.path.dirname(__file__)
DRIVERS_CSV = os.path.abspath(os.path.join(BASE, '..', 'data', 'drivers.csv'))
TRUCKS_CSV = os.path.abspath(os.path.join(BASE, '..', 'data', 'trucks.csv'))

conn = get_connection()
if not conn:
    print("❌ Could not connect to database for seeding.")
    exit(1)

cur = conn.cursor()

# 3. Seed drivers
with open(DRIVERS_CSV, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Convert availability '1'/'0' to Boolean
        is_avail = bool(int(row['is_available'])) if row['is_available'].isdigit() else True
        cur.execute("""
            INSERT INTO drivers (id, name, phone, is_available)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (int(row['id']), row['name'], row['phone'], is_avail))

# 4. Seed trucks
with open(TRUCKS_CSV, newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        is_avail = bool(int(row['is_available'])) if row['is_available'].isdigit() else True
        cur.execute("""
            INSERT INTO trucks (id, truck_number, fuel_efficiency, is_available)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (int(row['id']), row['registration_number'], float(row['fuel_efficiency']), is_avail))

conn.commit()
cur.close()
conn.close()
print("✅ Seeded drivers and trucks successfully.")

