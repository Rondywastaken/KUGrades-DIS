import re
from flask import Flask, render_template, request, abort, jsonify
from livereload import Server
import query

# Mirrors the institutions dict from setup.py
INSTITUTIONS = {
    65718: "Biologisk Institut",
    1932:  "Datalogisk Institut",
    2245:  "Institut for Fødevare- og Ressourceøkonomi",
    1915:  "Institut for Geovidenskab og Naturforvaltning",
    1950:  "Institut for Idræt og Ernæring",
    1869:  "Institut for Matematiske Fag",
    2160:  "Institut for Naturfagenes Didaktik",
    2238:  "Institut for Plante- og Miljøvidenskab",
    1568:  "Kemisk Institut",
    65707: "Niels Bohr Institutet",
}

app = Flask(__name__)

@app.template_filter('term_label')
def term_label(term):
    m = re.match(r'[a-zA-Z]*(\d+)/B(\d+)', term)
    if not m:
        return term
    year = int(m.group(1))
    block = m.group(2)
    full_year = 2000 + year if year < 100 else year
    return f"{full_year} · Block {block}"

# exam row column indices (SELECT * FROM exam):
# 0 course_id, 1 term, 2 exam_type, 3 attended, 4 registered, 5 passed,
# 6 grade_12, 7 grade_10, 8 grade_7, 9 grade_4, 10 grade_02, 11 grade_00,
# 12 grade_minus3, 13 ej_mødt, 14 ej_bedømt

def _calc_avg(row):
    weighted = (12*row[6] + 10*row[7] + 7*row[8] + 4*row[9]
                + 2*row[10] + 0*row[11] + (-3)*row[12])
    total = row[6] + row[7] + row[8] + row[9] + row[10] + row[11] + row[12]
    if total == 0:
        return None
    return round(weighted / total, 1)

def _build_exam(row):
    attended  = row[3] or 0
    registered = row[4] or 0
    passed    = row[5] or 0
    avg       = _calc_avg(row)
    pass_rate = round(passed / attended * 100, 1) if attended > 0 else 0.0
    return {
        "term":       row[1],
        "registered": registered,
        "attended":   attended,
        "passed":     passed,
        "avg":        avg,
        "pass_rate":  pass_rate,
        "grades": {
            "-3": row[12],
            "00": row[11],
            "02": row[10],
            "4":  row[9],
            "7":  row[8],
            "10": row[7],
            "12": row[6],
        },
    }

@app.route("/api/search")
def api_search():
    q = request.args.get("q", "").strip()
    if len(q) < 2:
        return jsonify([])
    raw = query.get_courses(q)
    return jsonify([{"id": r[0], "name": r[2]} for r in raw[:8]])

@app.route("/")
def index():
    q = request.args.get("q", "").strip()
    results = []
    if q:
        raw = query.get_courses(q)
        for r in raw:
            latest = query.get_latest_exam(r[0])
            exam = _build_exam(latest[0]) if latest else None
            results.append({
                "id":          r[0],
                "name":        r[2],
                "ects":        r[3],
                "institution": INSTITUTIONS.get(r[1], str(r[1])),
                "exam":        exam,
            })
    return render_template("index.html", results=results, q=q)

@app.route("/course/<course_id>")
def course_detail(course_id):
    # Fetch course row via search, then match exact ID
    matches = query.get_courses(course_id)
    course_row = next((r for r in matches if r[0].lower() == course_id.lower()), None)
    if not course_row:
        abort(404)

    course = {
        "id":          course_row[0],
        "name":        course_row[2],
        "institution": INSTITUTIONS.get(course_row[1], str(course_row[1])),
        "ects":        course_row[3],
    }

    term_rows = query.get_term_for_course(course_id)  # [(term,), ...]

    terms = []
    for term_row in term_rows:
        term = term_row[0]
        rows = query.get_exam_by_term(course_id, term)
        exam_row   = next((r for r in rows if r[2] == 'o'), None)
        reexam_row = next((r for r in rows if r[2] == 'r'), None)
        terms.append({
            "term":   term,
            "exam":   _build_exam(exam_row)   if exam_row   else None,
            "reexam": _build_exam(reexam_row) if reexam_row else None,
        })

    exam_avgs = [t['exam']['avg'] for t in terms if t['exam'] and t['exam']['avg'] is not None]
    latest_avg     = exam_avgs[0] if exam_avgs else None
    all_time_avg   = round(sum(exam_avgs) / len(exam_avgs), 1) if exam_avgs else None
    latest_pass    = terms[0]['exam']['pass_rate'] if terms and terms[0]['exam'] else None
    trend = ("up"   if len(exam_avgs) >= 2 and exam_avgs[0] > exam_avgs[1] else
             "down" if len(exam_avgs) >= 2 and exam_avgs[0] < exam_avgs[1] else "flat")

    stats = {
        "latest_avg":  latest_avg,
        "all_time_avg": all_time_avg,
        "pass_rate":   latest_pass,
        "term_count":  len(term_rows),
        "trend":       trend,
    }

    charts = []
    for i, t in enumerate(terms):
        if t["exam"]:
            charts.append({
                "id": f"chart-{i}",
                "grades": t["exam"]["grades"],
                "absent": t["exam"]["registered"] - t["exam"]["attended"],
            })
        if t["reexam"]:
            charts.append({
                "id": f"reexam-chart-{i}",
                "grades": t["reexam"]["grades"],
                "absent": t["reexam"]["registered"] - t["reexam"]["attended"],
            })

    trend_points = [
        {"label": t["term"], "avg": t["exam"]["avg"]}
        for t in reversed(terms)
        if t["exam"] and t["exam"]["avg"] is not None
    ]

    return render_template(
        "course.html",
        course=course,
        terms=terms,
        stats=stats,
        charts=charts,
        trend_points=trend_points,
    )

if __name__ == "__main__":
    app.debug = True
    server = Server(app.wsgi_app)
    server.watch("templates/")
    server.watch("static/styles")
    server.watch("static/js")
    server.watch("app.py")
    server.serve(port=7070)
