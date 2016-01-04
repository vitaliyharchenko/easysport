# coding=utf-8
import sys
import os

import django


sys.path.extend(['/Dev/Django/sportcourts'])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sportcourts.settings")
django.setup()

from courts.models import Court, CourtType
from places.models import Place, City, Country, Region
from sports.models import SportType, GameType, Amplua


print('Creating places...')
Country.objects.create(title=u'Россия')
Region.objects.create(title=u'Свердловская область', country=Country.objects.get(title=u'Россия'))
City.objects.create(title=u'Екатеринбург', region=Region.objects.get(title=u'Свердловская область'))
CourtType.objects.create(title=u'Крытая')
CourtType.objects.create(title=u'Открытая')


print('Creating sport types...')
SportType.objects.create(title=u'Баскетбол')
SportType.objects.create(title=u'Волейбол')
SportType.objects.create(title=u'Футбол')


print('Creating game types...')
GameType.objects.create(title=u'Открытая игра 5х5', sporttype=SportType.objects.get(title=u'Баскетбол'))
GameType.objects.create(title=u'Стритбол 3х3', sporttype=SportType.objects.get(title=u'Баскетбол'))

print('Creating ampluas...')
Amplua.objects.create(title=u'Центровой', sporttype=SportType.objects.get(title=u'Баскетбол'))
Amplua.objects.create(title=u'Нападающий', sporttype=SportType.objects.get(title=u'Баскетбол'))
