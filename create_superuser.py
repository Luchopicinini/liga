import os
import django
import sys

# Agregar el path del proyecto a PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # si create_superuser.py está en la raíz
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'liga_futbol.settings')

django.setup()

from django.contrib.auth.models import User

# Crear superusuario si no existe
if not User.objects.filter(username='luciano').exists():
    User.objects.create_superuser('luciano', 'tu@email.com', '123456789')
    print("Superusuario creado")
else:
    print("Superusuario ya existe")
