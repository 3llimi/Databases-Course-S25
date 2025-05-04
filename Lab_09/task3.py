import psycopg2
from geopy.geocoders import Nominatim

DB_PARAMS = {
    "dbname": "demo",
    "user": "postgres",
    "password": "baha654123",
    "host": "localhost",
    "port": "5432"
}

conn = psycopg2.connect(**DB_PARAMS)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS Address (
        address_id SERIAL PRIMARY KEY,
        address_text TEXT NOT NULL,
        address_x DOUBLE PRECISION NOT NULL,
        address_y DOUBLE PRECISION NOT NULL
    );
""")
conn.commit()

cur.execute("SELECT * FROM get_valid_coordinates();")
coordinates = cur.fetchall()

geolocator = Nominatim(user_agent="geo_converter")

for airport_code, lat, lon in coordinates:
    location = geolocator.reverse((lon, lat), exactly_one=True)
    address_text = location.address if location else "Unknown"

    cur.execute("""
        INSERT INTO Address (address_text, address_x, address_y)
        VALUES (%s, %s, %s);
    """, (address_text, lon, lat))

conn.commit()
cur.close()
conn.close()
