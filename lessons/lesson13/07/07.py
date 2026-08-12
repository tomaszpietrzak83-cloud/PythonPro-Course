import json
import sqlite3
from pathlib import Path

parentPath = Path(__file__).resolve().parent
libraryPath = (parentPath.parent / "06" / "university.db").resolve()
newCoursesPath = parentPath / "courses.json"
newStudentsPath = parentPath / "students.json"

with newCoursesPath.open("r", encoding="utf-8") as coursesFile:
    availableCourses = json.load(coursesFile)


with newStudentsPath.open("r", encoding="utf-8") as studentsFile:
    newStudents = json.load(studentsFile)

with sqlite3.connect(libraryPath) as connection:
    cursor = connection.cursor()
    cursor.executemany(
        """
    INSERT OR IGNORE INTO courses (buildingName, numberOfClassroom) VALUES (?, ?)""",
        availableCourses,
    )
    cursor.executemany(
        """
    INSERT OR IGNORE INTO students (name, surname) VALUES (?, ?)""",
        newStudents,
    )
    connection.commit()
