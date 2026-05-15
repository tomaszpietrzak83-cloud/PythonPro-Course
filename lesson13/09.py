import sqlite3
from pathlib import Path
from random import randint, sample

parentPath = Path(__file__).resolve().parent
libraryPath = parentPath / "06" / "university.db"

with sqlite3.connect(libraryPath) as connection:
    cursor = connection.cursor()
    cursor.execute(
        """
    SELECT id FROM students
    """
    )
    studentsIDs = [student[0] for student in cursor.fetchall()]

    cursor.execute(
        """
    SELECT id FROM courses
    """
    )
    coursesIDs = [course[0] for course in cursor.fetchall()]

    for studentID in studentsIDs:
        numberOfCourses = randint(2, 5)

        chosenCourses = sample(coursesIDs, numberOfCourses)
        # chosenCourses = []
        # while len(chosenCourses) < numberOfCourses:
        #     courseID = coursesIDs[randint(0, len(coursesIDs) - 1)]
        #     if courseID not in chosenCourses:
        #         chosenCourses.append(courseID)

        cursor.executemany(
            """
        INSERT OR IGNORE INTO assignments (studentId, courseId) VALUES (?, ?)
        """,
            [(studentID, courseID) for courseID in chosenCourses],
        )

    # for cleaning the table
    # cursor.execute("""
    # DELETE FROM assignments
    # """)
