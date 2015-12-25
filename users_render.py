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

from urllib.request import urlopen
from io import BytesIO
from django.core.files import File
import hashlib

users = User.objects.all()
for user in users:
    password = user.password
    user.set_password(password)
    user.is_active = True
    user.save()
    user.last_login = timezone.now()
    user.save()

    avatar_url = u'http://sportcourts.ru/images/avatars/{}'.format(user.pk)
    response = urlopen(avatar_url)
    io = BytesIO(response.read())
    file = File(io)
    str = file.readlines()

    hashId = hashlib.md5()
    hashId.update(repr(str).encode('utf-8'))
    hash = hashId.hexdigest()

    if hash == '0a70ab0f26836cb1c759346d897493c9':
        print(u'False for user id:{}'.format(user.pk))
    else:
        user.avatar.save(u'avatar{}'.format(user.pk), file)

    user.save()