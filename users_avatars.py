# coding=utf-8
import sys
import os

from urllib.request import urlopen
from io import BytesIO
from django.core.files import File
import hashlib

import django

# TODO: other sys path extend for production
sys.path.extend(['/Dev/Django/sportcourts'])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sportcourts.settings")
django.setup()

from users.models import User

user = User.objects.get(pk=1)
response = urlopen('http://sportcourts.ru/images/avatars/30')
io = BytesIO(response.read())
file = File(io)
str = file.readlines()

hashId = hashlib.md5()
hashId.update(repr(str).encode('utf-8'))
hash = hashId.hexdigest()

if hash == '0a70ab0f26836cb1c759346d897493c9':
    print('False')
else:
    user.avatar.save('avatar1', file)


