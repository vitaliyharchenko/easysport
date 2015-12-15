# coding=utf-8
from __future__ import unicode_literals
from django.db import models
from utils.fields import PhoneField
from sportcourts import settings


# Create your models here.
class Country(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название', unique=True)

    class Meta():
        verbose_name = 'страна'
        verbose_name_plural = 'страны'
        app_label = 'courts'

    def __str__(self):
        return u'{}'.format(self.title)


class Region(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название', unique=True)
    country = models.ForeignKey(Country)

    class Meta():
        verbose_name = 'область'
        verbose_name_plural = 'области'
        app_label = 'courts'

    def __str__(self):
        return u'{}'.format(self.title)


class City(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название', unique=True)
    region = models.ForeignKey(Region)

    class Meta():
        verbose_name = 'город'
        verbose_name_plural = 'города'
        app_label = 'courts'

    def __str__(self):
        return self.title


class Place(models.Model):
    city = models.ForeignKey(City)
    longitude = models.FloatField(verbose_name='Долгота', help_text='Возьмите из Яндекс карт')
    latitude = models.FloatField(verbose_name='Широта', help_text='Возьмите из Яндекс карт')
    fulladdress = models.CharField(max_length=500, verbose_name='Адрес', unique=True, help_text='В формате "ул. Московская, д.9"')

    class Meta():
        verbose_name = 'место'
        verbose_name_plural = 'места'
        app_label = 'courts'

    def __str__(self):
        return u'{}, {}'.format(self.city, self.fulladdress)

    # FIXME: save coords
    # def save(self):
    #     api_key = settings.YANDEX_MAPS_API_KEY
    #     pos = api.geocode(api_key, self.fulladdress)
    #     self.longitude = pos[0]
    #     self.latitude = pos[1]
    #     self.save_base()


class CourtType(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='Название типа площадки')

    class Meta():
        verbose_name = 'тип площадки'
        verbose_name_plural = 'типы площадок'
        app_label = 'courts'

    def __str__(self):
        return self.title


class Cover(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='Название типа покрытия')

    class Meta():
        verbose_name = 'тип покрытия'
        verbose_name_plural = 'типы покрытий'
        app_label = 'courts'

    def __str__(self):
        return self.title


class Worktime(models.Model):
    timefrom = models.TimeField(verbose_name='Начало работы')
    timeto = models.TimeField(verbose_name='Конец работы')

    class Meta():
        app_label = 'courts'

    def __str__(self):
        return u'с {} до {}'.format(self.timefrom, self.timeto)


class Court(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название', unique=True)
    description = models.CharField(max_length=300, verbose_name='Описание')
    admin_description = models.CharField(max_length=200, blank=True, verbose_name='Примечания для админов')
    place = models.ForeignKey(Place, verbose_name='Место')

    type = models.ForeignKey(CourtType, verbose_name='Тип площадки', related_name='+', null=True)
    # TODO: adding worktime and cover
    # worktime = models.ForeignKey(Worktime, verbose_name='Режим работы', blank=True, null=True)
    # cover = models.ForeignKey(Cover, verbose_name='Покрытие', blank=True, null=True)

    phone = PhoneField(verbose_name='Телефон', blank=True)

    max_players = models.IntegerField(verbose_name='Максимальное количество игроков', default=0)

    cost = models.IntegerField(verbose_name='Стоимость аренды, RUB/час', default=0)
    photo = models.ImageField(upload_to='courts', verbose_name='Изображение', blank=True, null=True)
    # sporttypes = models.ManyToManyField('events.SportType', verbose_name=u'Типы спорта', blank=True)
    views = models.IntegerField(default=0)

    class Meta():
        verbose_name = 'площадка'
        verbose_name_plural = 'площадки'
        app_label = 'courts'
        ordering = ['-views']

    def get_absolute_url(self):
        return "/courts/%i" % self.id

    def __str__(self):
        return self.title