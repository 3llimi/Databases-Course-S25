MATCH (p:Person)-[:ACTED_IN]->(actedMovie:Movie)
MATCH (p)-[:DIRECTED]->(directedMovie:Movie)
WITH p, 
     COUNT(DISTINCT actedMovie) AS actingCount,
     COUNT(DISTINCT directedMovie) AS directingCount,
     COLLECT(DISTINCT actedMovie.title) AS actedInMovies,
     COLLECT(DISTINCT directedMovie.title) AS directedMovies
RETURN p.name AS Person,
       actingCount AS MoviesActedIn,
       directingCount AS MoviesDirected,
       actedInMovies,
       directedMovies
ORDER BY directingCount DESC, actingCount DESC