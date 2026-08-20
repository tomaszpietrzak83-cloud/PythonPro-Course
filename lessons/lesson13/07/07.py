import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from help_functions import sql_query_executioner

parentPath = Path(__file__).resolve().parent
libraryPath = (parentPath.parent / "06" / "university.db").resolve()
newCoursesPath = parentPath / "courses.json"
newStudentsPath = parentPath / "students.json"

with newCoursesPath.open("r", encoding="utf-8") as coursesFile:
    availableCourses = json.load(coursesFile)

with newStudentsPath.open("r", encoding="utf-8") as studentsFile:
    newStudents = json.load(studentsFile)

query_available_courses = """--sql 
INSERT OR IGNORE INTO courses (buildingName, numberOfClassroom) VALUES (?, ?) 
"""
query_new_students = """--sql 
INSERT OR IGNORE INTO students (name, surname) VALUES (?, ?) 
"""

sql_query_executioner(query_available_courses, availableCourses, libraryPath)
sql_query_executioner(query_new_students, newStudents, libraryPath)
