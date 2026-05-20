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