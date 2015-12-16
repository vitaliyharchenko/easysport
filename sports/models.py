# coding=utf-8
from django.db import models


# Create your models here.
class SportType(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name='Название вида спорта')

    class Meta():
        verbose_name = 'Вид спорта'
        verbose_name_plural = 'Виды спорта'
        app_label = 'sports'

    def __str__(self):
        return self.title


class GameType(models.Model):
    sporttype = models.ForeignKey(SportType, verbose_name='Вид спорта')
    title = models.CharField(max_length=100, verbose_name='Название типа игры')

    class Meta():
        verbose_name = 'Тип игры'
        verbose_name_plural = 'Типы игры'
        app_label = 'sports'

    def __str__(self):
        return u'{} - {}'.format(self.sporttype.title, self.title)


class Amplua(models.Model):
    sporttype = models.ForeignKey(SportType, verbose_name='Вид спорта', related_name='+')
    title = models.CharField(max_length=100, verbose_name='Название')

    class Meta():
        verbose_name = 'амплуа'
        verbose_name_plural = 'амплуа'
        app_label = 'sports'

    def __str__(self):
        return u'{} - {}'.format(self.sporttype.title, self.title)