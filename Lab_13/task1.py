import psycopg2
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

conn = psycopg2.connect(
    dbname="writersDB",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

search_names = ["Alex", "Laura"]

for name in search_names:
    print(f"\nTop 5 writers similar to '{name}':\n")
    name_vec = model.encode(name).tolist()

    cur.execute("""
        SELECT name, text
        FROM writers
        ORDER BY name_vector <#> %s
        LIMIT 5
    """, (name_vec,))

    results = cur.fetchall()
    for r_name, r_text in results:
        print(f"Name: {r_name}")
        print(f"Text: {r_text[:200]}...\n")

cur.close()
conn.close()
