MATCH (p:Person)-[r:REVIEWED]->(m:Movie)
WHERE r.rating > 90
RETURN p.name AS Reviewer, 
       m.title AS Movie, 
       r.rating AS Rating,
       r.summary AS ReviewSummary
ORDER BY r.rating DESC