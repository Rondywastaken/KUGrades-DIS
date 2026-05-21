-- Unused legacy query: averages per grade column, not the weighted exam average.
-- Weighted averages are computed in utils/course_service.py from grade counts.
SELECT
    AVG(grade_12) AS avg_12,
    AVG(grade_10) AS avg_10,
    AVG(grade_7) AS avg_7,
    AVG(grade_4) AS avg_4,
    AVG(grade_00) AS avg_00,
    AVG(grade_minus3) AS avg_minus3
FROM exam
WHERE course_id = %s AND exam_type = 'o';
