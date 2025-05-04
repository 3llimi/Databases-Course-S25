import psycopg2
import string
from collections import Counter

conn = psycopg2.connect(
    dbname="writersDB",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

cursor.execute("SELECT text FROM writers;")
texts = cursor.fetchall()

stopwords = {
    "a", "an", "the", "and", "or", "but", "of", "to", "in", "on", "at", 
    "for", "by", "with", "as", "is", "are", "was", "were", "be", "been", "being"
}

keywords = []
for (text,) in texts:
    words = text.split()[:15]
    # Process each word
    for word in words:
        # Remove punctuation and lowercase
        cleaned_word = word.strip(string.punctuation).lower()
        # Filter out stopwords and empty strings
        if cleaned_word and cleaned_word not in stopwords:
            keywords.append(cleaned_word)

# Count keyword frequencies
keyword_counter = Counter(keywords)
top_keywords = keyword_counter.most_common(10)

#Solution
print("Top 10 Common Keywords:")
for keyword, count in top_keywords:
    print(f"{keyword}: {count} occurrences")

cursor.close()
conn.close()