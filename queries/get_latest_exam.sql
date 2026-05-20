SELECT * FROM exam
WHERE course_id = %s ORDER BY term DESC LIMIT 1;