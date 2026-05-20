SELECT * FROM courses 
WHERE course_id ILIKE %s OR name ILIKE %s;