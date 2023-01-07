import sys
import MySQLdb
import json

# Verify that four arguments were passed
if len(sys.argv) != 5:
    print("Usage: python dumpvehicles.py <host> <user> <password> <database>")
    sys.exit(1)

# Get arguments
host     = sys.argv[1]
user     = sys.argv[2]
password = sys.argv[3]
database = sys.argv[4]

# Open database connection
db = MySQLdb.connect(host, user, password, database)
cursor = db.cursor()

# Get table columns names
cursor.execute("SHOW COLUMNS FROM vehicles_metadata")
columns = [column[0] for column in cursor.fetchall()]

cursor.execute("SELECT * FROM vehicles_metadata")
data = cursor.fetchall()

vehicles = {}
for vehicle in data:
    
    vehicle = dict(zip(columns, vehicle))
    model = vehicle['model']
    # Remove None values and model key
    vehicle = {k: v for k, v in vehicle.items() if v is not None and k != 'model'}
    # Replace colon and forward slash in the realname with commas
    if "realname" in vehicle: vehicle['realname'] = vehicle['realname'].replace(';', ', ').replace('/', ', ')
    vehicles[model] = vehicle

# Save to JSON file with utf-8 encoding
with open('vehicles.json', 'w', encoding='utf-8') as f:
    json.dump(vehicles, f, ensure_ascii=False, indent=4)
    print(f"Saved {len(vehicles)} vehicles to vehicles.json")