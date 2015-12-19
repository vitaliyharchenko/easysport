# coding=utf-8
import sys
import os

import django

# TODO: other sys path extend for production
sys.path.extend(['/Dev/Django/sportcourts'])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sportcourts.settings")
django.setup()

from users.models import User

users = User.objects.all()
for user in users:
    password = user.password
    user.set_password(password)
    user.save()

u = User.objects.get(pk=1)
u.is_superuser = True
u.is_staff = True
u.save()