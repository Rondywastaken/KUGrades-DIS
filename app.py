import re
from flask import Flask, render_template
from livereload import Server

app = Flask(__name__)

@app.template_filter('term_label')
def term_label(term):
    """Convert 'v25/B2' → '2025 · Block 2'."""
    m = re.match(r'[a-zA-Z]*(\d+)/B(\d+)', term)
    if not m:
        return term
    year = int(m.group(1))
    block = m.group(2)
    full_year = 2000 + year if year < 100 else year
    return f"{full_year} · Block {block}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/course/<course_id>")
def course_detail(course_id):
    # Stub — replace with DB queries once backend is ready
    course = {
        "id": course_id,
        "name": "Algorithms and Data Structures",
        "institution": "Datalogisk Institut",
        "ects": 7.5,
    }
    terms = [
        {
            "term": "v25/B2",
            "exam": {
                "registered": 202, "attended": 173, "passed": 129, "failed": 44,
                "pass_rate": 74.6, "avg": 4.4,
                "grades": {"-3": 11, "00": 30, "02": 37, "4": 25, "7": 33, "10": 14, "12": 20},
            },
            "reexam": {
                "registered": 43, "attended": 43, "passed": 26, "failed": 17,
                "pass_rate": 60.5, "avg": 2.1,
                "grades": {"-3": 3, "00": 14, "02": 21, "4": 5, "7": 0, "10": 0, "12": 0},
            },
        },
        {
            "term": "v24/B2",
            "exam": {
                "registered": 226, "attended": 205, "passed": 157, "failed": 48,
                "pass_rate": 76.6, "avg": 5.1,
                "grades": {"-3": 6, "00": 40, "02": 27, "4": 40, "7": 45, "10": 24, "12": 21},
            },
            "reexam": None,
        },
        {
            "term": "v23/B1",
            "exam": None,
            "reexam": None,
        },
    ]
    stats = {
        "latest_avg": 4.4, "all_time_avg": 5.1,
        "pass_rate": 74.6, "term_count": 3, "trend": "down",
    }
    return render_template("course.html", course=course, terms=terms, stats=stats)

if __name__ == "__main__":
    app.debug = True 
    server = Server(app.wsgi_app)
    server.watch("templates/")
    server.watch("static/styles")
    server.watch("static/scripts")
    server.watch("app.py")
    server.serve(port=7070)
