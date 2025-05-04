MATCH (actor:Person)-[:ACTED_IN]->(movie:Movie)
WITH actor, 
     COLLECT(DISTINCT movie.released) AS releaseYears
WITH actor, 
     releaseYears,
     [year in releaseYears | toInteger(floor(year/10)*10)] AS decades
WITH actor, 
     releaseYears,
     apoc.coll.toSet(decades) AS uniqueDecades
WHERE size(uniqueDecades) >= 3
RETURN actor.name AS Actor,
       size(releaseYears) AS TotalMovies,
       apoc.coll.min(releaseYears) AS FirstYear,
       apoc.coll.max(releaseYears) AS LastYear,
       apoc.coll.max(releaseYears) - apoc.coll.min(releaseYears) AS CareerSpanYears,
       size(uniqueDecades) AS DecadesActive,
       uniqueDecades AS Decades
ORDER BY DecadesActive DESC, CareerSpanYears DESC