MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
WITH p, m ORDER BY m.released ASC
WITH p, head(collect(m)) AS earliest_movie
WHERE earliest_movie.released < 1990
RETURN p.name AS Actor, 
       earliest_movie.title AS Earliest_Movie, 
       earliest_movie.released AS Year
ORDER BY Year ASC