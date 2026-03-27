Upon cloning the git repository, you should run the following commands in the following order:
- python manage.py runserver
- python manage.py migrate
- python manage.py migrate game 0004_adminprofile --fake
- python manage.py migrate

After these steps have been completed, the database can be populated correctly.
To add art to the game, log in as an admin (using one of our GUIDs) and go to "Manage Artworks". From there you can upload files to the game!