migrations = """
Tomek@Tomek MINGW64 ~/Documents/Developer/Lesson 19/mojprojekt (master)
$ python manage.py makemigrations
Migrations for 'announcements':
  announcements\migrations\0001_initial.py
    + Create model Announcement
Migrations for 'blog':
  blog\migrations\0001_initial.py
    + Create model Post
(.venv) 
Tomek@Tomek MINGW64 ~/Documents/Developer/Lesson 19/mojprojekt (master)
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, announcements, auth, blog, contenttypes, sessions
Running migrations:
  Applying announcements.0001_initial... OK
  Applying blog.0001_initial... OK
"""
