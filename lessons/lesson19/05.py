superuser_creation = """
python manage.py createsuperuser
Username (leave blank to use 'tomek'): 
Email address: 
Password: 
Password (again): 
Error: Your passwords didn't match.
Password: 
Password (again): 
This password is too short. It must contain at least 8 characters.
This password is too common.
Bypass password validation and create user anyway? [y/N]: N
Password: 
Password (again): 
Superuser created successfully.
"""

superuser_login = "successfully logged in as superuser"
