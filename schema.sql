DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS exam;
DROP TABLE IF EXISTS course_term;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS institutions;


CREATE TABLE institutions (
    institution_id INTEGER,
    name CHAR(255),
    PRIMARY KEY (institution_id)
);

CREATE TABLE courses (
    course_id CHAR(255),
    institution_id INTEGER,
    name CHAR(255),
    ects INTEGER,
    PRIMARY KEY (course_id),
    FOREIGN KEY (institution_id) REFERENCES institutions ON DELETE CASCADE
);

CREATE TABLE course_term (
    course_id CHAR(255),
    term CHAR(20),
    PRIMARY KEY (course_id, term),
    FOREIGN KEY (course_id) REFERENCES courses ON DELETE CASCADE
    );

CREATE TABLE exam (
    course_id CHAR(255),
    term CHAR(20),
    exam_type CHAR(4),
    attended INTEGER,
    registered INTEGER,
    passed INTEGER,
    failed INTEGER,
    PRIMARY KEY (course_id, term, exam_type),
    FOREIGN KEY (course_id, term) REFERENCES course_term ON DELETE CASCADE
);

CREATE TABLE grades (
    course_id CHAR(255),
    term CHAR(50),
    exam_type CHAR(4),
    grade_12 INTEGER,
    grade_10 INTEGER,
    grade_7 INTEGER,
    grade_4 INTEGER,
    grade_02 INTEGER,
    grade_00 INTEGER,
    grade_minus3 INTEGER,
    ej_mødt INTEGER,
    ikke_bestået INTEGER, 
    PRIMARY KEY (course_id, term, exam_type),
    FOREIGN KEY (course_id, term, exam_type) REFERENCES exam ON DELETE CASCADE
);
