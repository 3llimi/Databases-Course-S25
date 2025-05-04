CREATE VIEW unoverridden_fails AS
SELECT t1.*
FROM takes t1
WHERE t1.grade = 'F' 
  AND NOT EXISTS (
    SELECT 1
    FROM takes t2
    WHERE t2.ID = t1.ID 
      AND t2.course_id = t1.course_id 
      AND t2.sec_id = t1.sec_id 
      AND t2.semester = t1.semester
      AND t2.year = t1.year
      AND t2.grade IN ('A', 'B', 'C', 'D')
  );
