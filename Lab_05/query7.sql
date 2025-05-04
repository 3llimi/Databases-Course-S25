SELECT COUNT(t.id) AS num_students
FROM takes t
WHERE (t.course_id, t.sec_id, t.semester) = (
    SELECT s.course_id, s.sec_id, s.semester
    FROM section s
    LEFT JOIN takes t2 
        ON s.course_id = t2.course_id 
        AND s.sec_id = t2.sec_id 
        AND s.semester = t2.semester
    WHERE s.semester IN ('Spring')
    GROUP BY s.course_id, s.sec_id, s.semester
    ORDER BY COUNT(t2.id) DESC
    LIMIT 1
);
