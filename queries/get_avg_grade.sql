SELECT
    AVG(grade_12) AS avg_12,
    AVG(grade_10) AS avg_10,
    AVG(grade_7) AS avg_7,
    AVG(grade_4) AS avg_4,
    AVG(grade_00) AS avg_00,
    AVG(grade_minus3) AS avg_minus3
FROM exam WHERE course_id = %s
