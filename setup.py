# Script to populate database with data source which is in json format

import psycopg2
import json
import os

institutions = {
    65718: "Biologisk Institut",
    1932: "Datalogisk Institut",
    2245: "Institut for Fødevare- og Ressourceøkonomi",
    1915: "Institut for Geovidenskab og Naturforvaltning",
    1950: "Institut for Idræt og Ernæring",
    1869: "Institut for Matematiske Fag",
    2160: "Institut for Naturfagenes Didaktik",
    2238: "Institut for Plante- og Miljøvidenskab",
    1568: "Kemisk Institut",
    65707: "Niels Bohr Institutet"
}

directory = "./data"
if not os.path.isdir(directory):
  print("data source directory does not exists. Download data source as 'data/' folder first")
  exit()

def insert_exam(cur, course_id, term, exam_type, attended, registered, passed, grades):
  is_pass_fail = "Bestået" in grades
  cur.execute(
    """
    INSERT INTO exam (
      course_id, term, exam_type,
      attended, registered, passed,
      grade_12, grade_10, grade_7, grade_4, grade_02, grade_00, grade_minus3, ej_mødt, ej_bedømt
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """,
    (
      course_id, term, exam_type, attended, registered, passed,
      None if is_pass_fail else grades.get("12", 0),
      None if is_pass_fail else grades.get("10", 0),
      None if is_pass_fail else grades.get("7", 0),
      None if is_pass_fail else grades.get("4", 0),
      None if is_pass_fail else grades.get("02", 0),
      None if is_pass_fail else grades.get("00", 0),
      None if is_pass_fail else grades.get("-3", 0),
      grades.get("Ej mødt", 0),
      grades.get("Ej bedømt", 0)
    )
  )

try:
  database_url = os.environ.get("DATABASE_URL")
  if database_url:
    conn = psycopg2.connect(database_url)
  else:
    conn = psycopg2.connect(
      database="KUGrades",
      user="postgres",
      password="",
      host="localhost",
      port="5432"
    )
  cur = conn.cursor()

  for ins_id, ins_name in institutions.items():
    filepath = os.path.join(directory, f"{ins_name}.json")

    if not os.path.exists(filepath):
      print(f"Missing data source file: {filepath}, skipping but database will be incomplete")
      continue

    with open(filepath, encoding="utf-8") as f:
      data = json.load(f)

    cur.execute(
      """
      INSERT INTO institutions (institution_id, name)
      VALUES (%s, %s) 
      """,
      (ins_id, ins_name)
    )

    for key, value in data.items():
      course_id = key.split("-")[0]
      if course_id == "Histogram":
          course_id = key.split("-")[1]
      term = value["term"]
      ects = float(value["ects"].replace(",", "."))
      name = value["title"]
      
      cur.execute(
        """
        INSERT INTO courses (course_id, institution_id, name, ects)
        VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING
        """,
        (course_id, ins_id, name, ects)
      )

      cur.execute(
        """
        INSERT INTO course_term (course_id, term)
        VALUES (%s, %s) 
        """,
        (course_id, term)
      )

      if value.get("exam", False):
        insert_exam(
          cur,
          course_id,
          term,
          'o',
          value["attended"],
          value["registered"],
          value["passed"],
          value["grades"]
        )

      if value.get("reexam", False):
        insert_exam(
          cur,
          course_id,
          term,
          'r',
          value["attended_reexam"],
          value["registered_reexam"],
          value["passed_reexam"],
          value["grades_reexam"]
        )


  
  conn.commit()
  print("Populated database with data source")
  cur.close()
  conn.close()
except Exception as e:
  print(f"Error populating database: {e}")
