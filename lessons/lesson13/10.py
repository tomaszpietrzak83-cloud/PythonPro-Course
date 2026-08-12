import sqlite3
from pathlib import Path

parentPath = Path(__file__).resolve().parent
libraryPath = parentPath / "06" / "university.db"


def findStudentsNumbersOfClassrooms(surname: str) -> list[str]:
    return (
        """--sql
        SELECT courses.buildingName, courses.numberOfClassroom
        FROM courses
        JOIN assignments ON courses.id = assignments.courseId
        JOIN students ON assignments.studentId = students.id
        WHERE students.surname = ?""",
        (surname,),
    )


with sqlite3.connect(libraryPath) as conn:
    cursor = conn.cursor()
    cursor.execute(*findStudentsNumbersOfClassrooms("Wilson"))
    result = cursor.fetchall()
    print(result)
