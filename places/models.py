from django.db import models


# Create your models here.
class Country(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название', unique=True)

    class Meta():
        verbose_name = 'страна'
        verbose_name_plural = 'страны'
        app_label = 'places'

    def __str__(self):
        return u'{}'.format(self.title)


class Region(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название', unique=True)
    country = models.ForeignKey(Country)

    class Meta():
        verbose_name = 'область'
        verbose_name_plural = 'области'
        app_label = 'places'

    def __str__(self):
        return u'{}'.format(self.title)


class City(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название', unique=True)
    region = models.ForeignKey(Region)

    class Meta():
        verbose_name = 'город'
        verbose_name_plural = 'города'
        app_label = 'places'

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
        app_label = 'places'

    def __str__(self):
        return u'{}, {}'.format(self.city, self.fulladdress)

    # FIXME: save coords
    # def save(self):
    #     api_key = settings.YANDEX_MAPS_API_KEY
    #     pos = api.geocode(api_key, self.fulladdress)
    #     self.longitude = pos[0]
    #     self.latitude = pos[1]
    #     self.save_base()