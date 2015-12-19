# coding=utf-8
import sys
import os

import django


sys.path.extend(['/Dev/Django/sportcourts'])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sportcourts.settings")
django.setup()

from users.models import User

users = User.objects.all()
for user in users:
    password = user.password
    user.set_password(password)
    user.save()