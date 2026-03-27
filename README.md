Upon cloning the git repository, you should run the following commands in the following order:
- python manage.py runserver
- python manage.py migrate
- python manage.py migrate game 0004_adminprofile --fake
- python manage.py migrate

After these steps have been completed, the database can be populated correctly.