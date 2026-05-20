import psycopg2
import os

def connect_db():
    conn = psycopg2.connect(
        host = "..",
        dbname = "..",
        user = "..",
        password = "..", 
    )
    return conn.cursor()

def load_query(filename):
    path = os.path.join(os.path.dirname(__file__), "queries", filename)
    with open(path, "r") as f:
        return f.read()

def get_courses(search_course):
    query = load_query("get_course.sql")
    finding = f"%{search_course}%"
    cur = connect_db()
    cur.execute(query, (finding, finding))
    result = cur.fetchall()
    cur.close()
    return result

def get_latest_exam (course_id):
    query = load_query("get_latest_exam.sql")
    cur = connect_db()
    cur.execute(query, (course_id,))
    result = cur.fetchall()
    cur.close()
    return result

def get_exam_by_term (course_id, term):
    query = load_query("get_exam_by_term.sql")
    cur = connect_db()
    cur.execute(query, (course_id, term))
    result = cur.fetchall()
    cur.close()
    return result

def get_term_for_course (course_id):
    query = load_query("get_term_for_course.sql")
    cur = connect_db()
    cur.execute(query, (course_id,))
    result = cur.fetchall()
    cur.close()
    return result

def get_avg_grade (course_id):
    query = load_query("get_avg_grade.sql")
    cur = connect_db()
    cur.execute(query, (course_id,))
    result = cur.fetchall()
    cur.close
    return result