import os

import psycopg2
from flask import g, has_request_context


def _create_connection():
    return psycopg2.connect(database="kugrades")


def _get_connection():
    if has_request_context():
        conn = g.get("db_conn")
        if conn is None or conn.closed:
            conn = _create_connection()
            g.db_conn = conn
        return conn
    return _create_connection()


def close_db(_exception=None):
    conn = g.pop("db_conn", None)
    if conn is not None and not conn.closed:
        conn.close()


def init_app(app):
    app.teardown_appcontext(close_db)

def load_query(filename):
    path = os.path.join(os.path.dirname(__file__), "queries", filename)
    with open(path, "r") as f:
        return f.read()


def _execute_query(filename, params):
    conn = _get_connection()
    standalone = not has_request_context()
    cur = conn.cursor()
    try:
        cur.execute(load_query(filename), params)
        return cur.fetchall()
    finally:
        cur.close()
        if standalone:
            conn.close()


def get_courses(search_course):
    finding = f"%{search_course}%"
    return _execute_query("get_course.sql", (finding, finding))


def get_latest_exam(course_id):
    return _execute_query("get_latest_exam.sql", (course_id,))


def get_exam_by_term(course_id, term):
    return _execute_query("get_exam_by_term.sql", (course_id, term))


def get_term_for_course(course_id):
    return _execute_query("get_term_for_course.sql", (course_id,))


def get_avg_grade(course_id):
    return _execute_query("get_avg_grade.sql", (course_id,))
