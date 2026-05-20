DROP TABLE IF EXISTS exam;
DROP TABLE IF EXISTS course_term;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS institutions;

CREATE TABLE institutions (
  institution_id INTEGER,
  name TEXT,
  PRIMARY KEY (institution_id)
);

CREATE TABLE courses (
  course_id TEXT,
  institution_id INTEGER,
  name TEXT,
  ects FLOAT,
  PRIMARY KEY (course_id),
  FOREIGN KEY (institution_id) REFERENCES institutions ON DELETE CASCADE
);

CREATE TABLE course_term (
  course_id TEXT,
  term TEXT,
  PRIMARY KEY (course_id, term),
  FOREIGN KEY (course_id) REFERENCES courses ON DELETE CASCADE
);

CREATE TABLE exam (
  course_id TEXT,
  term TEXT,
  exam_type TEXT,
  attended INTEGER,
  registered INTEGER,
  passed INTEGER,
  grade_12 INTEGER,
  grade_10 INTEGER,
  grade_7 INTEGER,
  grade_4 INTEGER,
  grade_02 INTEGER,
  grade_00 INTEGER,
  grade_minus3 INTEGER,
  ej_mødt INTEGER,
  ej_bedømt INTEGER,
  PRIMARY KEY (course_id, term, exam_type),
  FOREIGN KEY (course_id, term) REFERENCES course_term ON DELETE CASCADE
);
