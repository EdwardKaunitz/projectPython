CTRl+ALT+SHIFT+H

admin
0000

C:\projectPython\my_project1>cd ..
C:\projectPython> project1\scripts\activate
C:\projectPython> project1\scripts\deactivate

(project1) C:\projectPython> cd my_project1           

python manage.py startapp _name_
python manage.py createsuperuser

python manage.py runserver
daphne my_project1.asgi:application

python manage.py makemigrations
python manage.py migrate


query = ModelNAme.objects.all() .get() .filter()