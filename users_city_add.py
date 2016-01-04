# coding=utf-8
import sys
import os

import django
from django.utils import timezone

# TODO: other sys path extend for production
sys.path.extend(['/Dev/Django/sportcourts'])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sportcourts.settings")
django.setup()

from users.models import User
from places.models import City

users = User.objects.all()
for user in users:
    user.city = City.objects.get(pk=1)
    user.save()
