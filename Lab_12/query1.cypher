MATCH (p:Person)-[r:ACTED_IN]->(m:Movie)
WHERE size(r.roles) > 1
RETURN p.name AS Actor, m.title AS Movie, r.roles AS Roles
ORDER BY size(r.roles) DESC