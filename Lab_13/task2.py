import random
import psycopg2
from pgvector.psycopg2 import register_vector
from sentence_transformers import SentenceTransformer

conn = psycopg2.connect(
    dbname="writersDB",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
register_vector(conn)
cursor = conn.cursor()

# Selecting a random writer
cursor.execute("SELECT writer_name, text FROM writers ORDER BY RANDOM() LIMIT 1;")
random_writer = cursor.fetchone()
print(f"Randomly Selected Writer: {random_writer[0]}\nText: {random_writer[1]}\n")

# Getting embedding for the random writer's text
model = SentenceTransformer('all-MiniLM-L6-v2')
random_text_vector = model.encode(random_writer[1]).tolist()

# Finding similar texts using cosine similarity
cursor.execute("""
    SELECT writer_name, text
    FROM writers
    WHERE id != %s  # Exclude the randomly selected writer
    ORDER BY text_vector <=> %s
    LIMIT 5;  # Adjust limit as needed
""", (random_writer[0], random_text_vector))

similar_writers = cursor.fetchall()

# Printing results
print("Similar Writers:")
for writer in similar_writers:
    print(f"Writer: {writer[0]}\nText: {writer[1]}\n{'-'*50}")

cursor.close()
conn.close()