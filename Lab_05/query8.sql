CREATE TABLE grade_mapping (
    grade VARCHAR(2) PRIMARY KEY,
    numeric_value INT
);

-- mappings of grades to numerical values
INSERT INTO grade_mapping VALUES ('A', 4);
INSERT INTO grade_mapping VALUES ('A-', 4);
INSERT INTO grade_mapping VALUES ('A+', 4);
INSERT INTO grade_mapping VALUES ('B', 3);
INSERT INTO grade_mapping VALUES ('B-', 3);
INSERT INTO grade_mapping VALUES ('B+', 3);
INSERT INTO grade_mapping VALUES ('C', 2);
INSERT INTO grade_mapping VALUES ('C-', 2);
INSERT INTO grade_mapping VALUES ('C+', 2);
INSERT INTO grade_mapping VALUES ('D', 1);
INSERT INTO grade_mapping VALUES ('D-', 1);
INSERT INTO grade_mapping VALUES ('D+', 1);
INSERT INTO grade_mapping VALUES ('F', 0);

SELECT s.id, s.name, 
       CASE 
           WHEN COUNT(t.grade) = 0 THEN NULL 
           ELSE AVG(g.numeric_value)        
       END AS GPA
FROM student s
LEFT JOIN takes t ON s.id = t.id 
LEFT JOIN grade_mapping g ON t.grade = g.grade
GROUP BY s.id, s.name;
