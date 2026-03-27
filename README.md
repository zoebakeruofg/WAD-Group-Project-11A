If you encounter the following migration error:

django.db.utils.OperationalError: table "game_adminprofile" already exists

Run the following commands to fix it:

python manage.py migrate game 0004_adminprofile --fake
python manage.py migrate
