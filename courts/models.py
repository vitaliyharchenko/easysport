# coding=utf-8
from __future__ import unicode_literals
from django.db import models
from utils.fields import PhoneField
from places.models import Place


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
        return "/court/%i" % self.id

    def __str__(self):
        return self.title