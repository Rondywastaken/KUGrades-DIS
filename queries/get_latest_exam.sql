-- Latest term's exam row: prefer ordinary ('o'), else re-exam ('r').
SELECT * FROM (
  SELECT DISTINCT ON (term) *
  FROM exam
  WHERE course_id = %s
  ORDER BY term DESC, exam_type ASC
) latest_term_exam
ORDER BY term DESC
LIMIT 1;
