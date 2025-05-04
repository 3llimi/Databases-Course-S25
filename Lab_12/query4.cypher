MATCH (director:Person)-[:DIRECTED]->(movie:Movie)<-[:ACTED_IN]-(actor:Person)
WITH director, actor, COLLECT(movie.title) AS movies, COUNT(movie) AS collaboration_count
WHERE collaboration_count > 2
RETURN director.name AS Director, 
       actor.name AS Actor, 
       collaboration_count AS MoviesTogether,
       movies AS Collaborations
ORDER BY collaboration_count DESC, Director, Actor