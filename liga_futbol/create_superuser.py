# create_superuser.py
from django.contrib.auth import get_user_model
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'liga_futbol.settings')
django.setup()

User = get_user_model()

# Cambia estos datos por el usuario y contraseña que quieras
USERNAME = "adminluciano"
EMAIL = "admin@example.com"
PASSWORD = "Liga2025!"

if not User.objects.filter(username=USERNAME).exists():
    User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
    print("Superusuario creado")
else:
    print("Superusuario ya existe")
