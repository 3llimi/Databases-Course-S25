import psycopg2
from sentence_transformers import SentenceTransformer
import re

model = SentenceTransformer('all-MiniLM-L6-v2')

conn = psycopg2.connect(
    dbname="writersDB",
    user="postgres",       
    password="postgres",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Create extension and table with vector columns
cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
cur.execute("DROP TABLE IF EXISTS writers;")
cur.execute("""
    CREATE TABLE writers (
        id SERIAL PRIMARY KEY,
        name TEXT,
        name_vector VECTOR(384),
        text TEXT,
        text_vector VECTOR(384)
    );
""")
conn.commit()

with open("writers_biographies.txt", "r", encoding="utf-8") as f:
    content = f.read()

entries = re.split(r'\n---\n', content.strip())
for entry in entries:
    match = re.match(r"# (.*?): (.*?)\n(.*)", entry, re.DOTALL)
    if not match:
        continue
    name = match.group(1).strip()
    title = match.group(2).strip()
    text = match.group(3).strip().replace("\n", " ")

    name_vec = model.encode(name).tolist()
    text_vec = model.encode(text).tolist()

    cur.execute("""
        INSERT INTO writers (name, name_vector, text, text_vector)
        VALUES (%s, %s, %s, %s)
    """, (name, name_vec, text, text_vec))

conn.commit()
cur.close()
conn.close()

print("Writers successfully added to the database.")
