import json
from pathlib import Path

parentPath = Path(__file__).resolve().parent
coursesPath = parentPath / "courses.json"
studentsPath = parentPath / "students.json"

availableCourses = [
    ("Main Building", 101),
    ("Main Building", 102),
    ("Science Building", 201),
    ("Science Building", 202),
    ("Arts Building", 301),
    ("Arts Building", 302),
    ("Engineering Building", 401),
    ("Engineering Building", 402),
    ("Business Building", 501),
    ("Business Building", 502),
    ("Law Building", 601),
    ("Law Building", 602),
    ("Medicine Building", 701),
    ("Medicine Building", 702),
    ("Education Building", 801),
    ("Education Building", 802),
    ("Music Building", 901),
    ("Music Building", 902),
    ("History Building", 1001),
    ("History Building", 1002),
]

newStudents = [
    ("John", "Smith"),
    ("Jane", "Doe"),
    ("Alice", "Johnson"),
    ("Bob", "Brown"),
    ("Charlie", "Davis"),
    ("Emily", "Wilson"),
    ("David", "Miller"),
    ("Sophia", "Taylor"),
    ("Michael", "Anderson"),
    ("Olivia", "Thomas"),
    ("William", "Jackson"),
    ("Ava", "White"),
    ("James", "Harris"),
    ("Isabella", "Martin"),
    ("Benjamin", "Thompson"),
    ("Mia", "Garcia"),
    ("Elijah", "Martinez"),
    ("Charlotte", "Robinson"),
    ("Lucas", "Clark"),
    ("Amelia", "Rodriguez"),
    ("Ethan", "Lewis"),
    ("Harper", "Lee"),
    ("Alexander", "Walker"),
    ("Evelyn", "Hall"),
    ("Jacob", "Allen"),
    ("Abigail", "Young"),
    ("Michael", "King"),
    ("Emily", "Wright"),
    ("Daniel", "Scott"),
    ("Sofia", "Green"),
    ("Matthew", "Adams"),
    ("Avery", "Baker"),
    ("Joseph", "Gonzalez"),
    ("Ella", "Nelson"),
    ("David", "Carter"),
    ("Madison", "Mitchell"),
    ("Samuel", "Perez"),
    ("Susan", "Roberts"),
    ("Andrew", "Turner"),
    ("Victoria", "Phillips"),
    ("Christopher", "Campbell"),
    ("Grace", "Parker"),
    ("Joshua", "Evans"),
    ("Chloe", "Edwards"),
    ("Nicholas", "Collins"),
    ("Lily", "Stewart"),
    ("Ryan", "Sanchez"),
    ("Zoe", "Morris"),
    ("Brandon", "Rogers"),
    ("Hannah", "Reed"),
    ("Justin", "Cook"),
    ("Lillian", "Morgan"),
    ("Kevin", "Bell"),
    ("Addison", "Murphy"),
]

with coursesPath.open("w", encoding="utf8") as coursesFile:
    json.dump(availableCourses, coursesFile, ensure_ascii=False, indent=4)

with studentsPath.open("w", encoding="utf8") as studentsFile:
    json.dump(newStudents, studentsFile, ensure_ascii=False, indent=4)
