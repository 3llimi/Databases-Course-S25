SELECT t.ID, s.name FROM unoverridden_fails t JOIN student s ON t.ID = s.ID GROUP BY t.ID, s.name HAVING COUNT(t.grade) >= 2;
