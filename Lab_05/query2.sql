SELECT s.ID, s.name FROM student s JOIN takes t ON s.ID = t.ID WHERE t.course_id = 'BIO-301';
