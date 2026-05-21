from flask import Flask, render_template, request, abort, jsonify
from livereload import Server

import query
from utils.course_service import get_course_detail, search_courses, search_suggestions
from utils.template_filters import term_label

app = Flask(__name__)
app.template_filter("term_label")(term_label)
query.init_app(app)


@app.route("/api/search")
def api_search():
    q = request.args.get("q", "").strip()
    if len(q) < 2:
        return jsonify([])
    return jsonify(search_suggestions(q))


@app.route("/")
def index():
    q = request.args.get("q", "").strip()
    results = search_courses(q) if q else []
    return render_template("index.html", results=results, q=q)


@app.route("/course/<course_id>")
def course_detail(course_id):
    detail = get_course_detail(course_id)
    if not detail:
        abort(404)

    return render_template(
        "course.html",
        course=detail["course"],
        terms=detail["terms"],
        stats=detail["stats"],
        charts=detail["charts"],
        trend_points=detail["trend_points"],
    )

if __name__ == "__main__":
    app.debug = True
    server = Server(app.wsgi_app)
    server.watch("templates/")
    server.watch("static/styles")
    server.watch("static/js")
    server.watch("app.py")
    server.watch("utils/course_service.py")
    server.watch("utils/template_filters.py")
    server.serve(port=7070)
