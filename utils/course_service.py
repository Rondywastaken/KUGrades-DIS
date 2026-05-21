import query


# Mirrors the institutions dict from setup.py
INSTITUTIONS = {
    65718: "Biologisk Institut",
    1932: "Datalogisk Institut",
    2245: "Institut for Fødevare- og Ressourceøkonomi",
    1915: "Institut for Geovidenskab og Naturforvaltning",
    1950: "Institut for Idræt og Ernæring",
    1869: "Institut for Matematiske Fag",
    2160: "Institut for Naturfagenes Didaktik",
    2238: "Institut for Plante- og Miljøvidenskab",
    1568: "Kemisk Institut",
    65707: "Niels Bohr Institutet",
}


def search_suggestions(search_term):
    raw_courses = query.get_courses(search_term)
    return [{"id": course[0], "name": course[2]} for course in raw_courses[:8]]


def search_courses(search_term):
    results = []
    for course_row in query.get_courses(search_term):
        latest = query.get_latest_exam(course_row[0])
        exam = _build_exam(latest[0]) if latest else None
        results.append({
            "id": course_row[0],
            "name": course_row[2],
            "ects": course_row[3],
            "institution": _institution_name(course_row[1]),
            "exam": exam,
        })
    return results


def get_course_detail(course_id):
    course_row = _find_course_by_id(course_id)
    if not course_row:
        return None

    terms = _get_terms(course_id)

    return {
        "course": _build_course(course_row),
        "terms": terms,
        "stats": _build_stats(terms),
        "charts": _build_charts(terms),
        "trend_points": _build_trend_points(terms),
    }


def _find_course_by_id(course_id):
    matches = query.get_courses(course_id)
    return next(
        (course for course in matches if course[0].lower() == course_id.lower()),
        None,
    )


def _build_course(course_row):
    return {
        "id": course_row[0],
        "name": course_row[2],
        "institution": _institution_name(course_row[1]),
        "ects": course_row[3],
    }


def _institution_name(institution_id):
    return INSTITUTIONS.get(institution_id, str(institution_id))


def _get_terms(course_id):
    terms = []
    for term_row in query.get_term_for_course(course_id):
        term = term_row[0]
        exam_rows = query.get_exam_by_term(course_id, term)
        exam_row = next((row for row in exam_rows if row[2] == "o"), None)
        reexam_row = next((row for row in exam_rows if row[2] == "r"), None)
        terms.append({
            "term": term,
            "exam": _build_exam(exam_row) if exam_row else None,
            "reexam": _build_exam(reexam_row) if reexam_row else None,
        })
    return terms


# exam row column indices (SELECT * FROM exam):
# 0 course_id, 1 term, 2 exam_type, 3 attended, 4 registered, 5 passed,
# 6 grade_12, 7 grade_10, 8 grade_7, 9 grade_4, 10 grade_02, 11 grade_00,
# 12 grade_minus3, 13 ej_mødt, 14 ej_bedømt
def _calculate_average(exam_row):
    weighted = (
        12 * exam_row[6]
        + 10 * exam_row[7]
        + 7 * exam_row[8]
        + 4 * exam_row[9]
        + 2 * exam_row[10]
        + 0 * exam_row[11]
        + (-3) * exam_row[12]
    )
    total = sum(exam_row[6:13])
    if total == 0:
        return None
    return round(weighted / total, 1)


def _build_exam(exam_row):
    attended = exam_row[3] or 0
    registered = exam_row[4] or 0
    passed = exam_row[5] or 0
    pass_rate = round(passed / attended * 100, 1) if attended > 0 else 0.0

    return {
        "term": exam_row[1],
        "registered": registered,
        "attended": attended,
        "passed": passed,
        "avg": _calculate_average(exam_row),
        "pass_rate": pass_rate,
        "grades": {
            "-3": exam_row[12],
            "00": exam_row[11],
            "02": exam_row[10],
            "4": exam_row[9],
            "7": exam_row[8],
            "10": exam_row[7],
            "12": exam_row[6],
        },
    }


def _build_stats(terms):
    exam_avgs = [
        term["exam"]["avg"]
        for term in terms
        if term["exam"] and term["exam"]["avg"] is not None
    ]
    latest_avg = exam_avgs[0] if exam_avgs else None
    all_time_avg = round(sum(exam_avgs) / len(exam_avgs), 1) if exam_avgs else None
    latest_pass = terms[0]["exam"]["pass_rate"] if terms and terms[0]["exam"] else None

    return {
        "latest_avg": latest_avg,
        "all_time_avg": all_time_avg,
        "pass_rate": latest_pass,
        "term_count": len(terms),
        "trend": _grade_trend(exam_avgs),
    }


def _grade_trend(exam_avgs):
    if len(exam_avgs) < 2:
        return "flat"
    if exam_avgs[0] > exam_avgs[1]:
        return "up"
    if exam_avgs[0] < exam_avgs[1]:
        return "down"
    return "flat"


def _build_charts(terms):
    charts = []
    for index, term in enumerate(terms):
        if term["exam"]:
            charts.append(_build_chart(f"chart-{index}", term["exam"]))
        if term["reexam"]:
            charts.append(_build_chart(f"reexam-chart-{index}", term["reexam"]))
    return charts


def _build_chart(chart_id, exam):
    return {
        "id": chart_id,
        "grades": exam["grades"],
        "absent": exam["registered"] - exam["attended"],
    }


def _build_trend_points(terms):
    return [
        {"label": term["term"], "avg": term["exam"]["avg"]}
        for term in reversed(terms)
        if term["exam"] and term["exam"]["avg"] is not None
    ]
