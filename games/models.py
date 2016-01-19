# coding=utf-8
import datetime
from django.utils import timezone
from django.db import models
from courts.models import Court
from sports.models import GameType, SportType
from django.contrib.contenttypes.models import ContentType
from utils import formatters, validators


class Game(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.CharField(max_length=300, verbose_name='Описание')

    # TODO: add image of event
    is_public = models.BooleanField('Публичный статус', default=True,
                                    help_text="Делает видимым в потоке")

    responsible_user = models.ForeignKey('users.User', related_name='events_responsible',
                                         limit_choices_to={'is_responsible': True},
                                         verbose_name='Ответственный')
    # auto define in admin.py
    created_by = models.ForeignKey('users.User', blank=True, null=True)
    # может быть, а может и не быть тренер на игре
    coach = models.ForeignKey('users.User', related_name='coach', blank=True, null=True,
                              limit_choices_to={'is_coach': True})

    court = models.ForeignKey(Court, verbose_name='Площадка')

    gametype = models.ForeignKey(GameType, verbose_name='Тип игры')
    sporttype = models.ForeignKey(SportType, verbose_name='Вид спорта', blank=True, null=True)

    capacity = models.IntegerField(verbose_name='Вместимость', help_text='введите 0 для безлимитной игры')

    cost = models.PositiveIntegerField(verbose_name='Цена')

    datetime = models.DateTimeField(verbose_name='Дата проведения')
    datetime_to = models.DateTimeField(verbose_name='Дата окончания', blank=True)

    reserved_count = models.PositiveIntegerField(verbose_name='Резервных мест', default=0)
    deleted = models.BooleanField(default=False, verbose_name='Игра удалена')
    is_reported = models.BooleanField(verbose_name='Отчет отправлен', default=False)

    class Meta():
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'
        ordering = ['-datetime']
        get_latest_by = 'datetime'
        app_label = 'games'

    def __str__(self):
        return u'Игра №{}, {}, {}'.format(self.id, self.datetime, self.court)

    def __unicode__(self):
        return u'Игра №{}, {}, {}'.format(self.id, self.datetime, self.court)

    def save(self):
        if self.datetime > self.datetime_to:
            raise ValueError('Проверьте отрезки времени')
        self.save_base()

    # TODO: логика удаления игры

    def old_users(self):
        court = self.court
        sporttype = self.sport_type
        games = Game.objects.filter(court=court, sporttype_id=sporttype, is_reported=True)
        old_users = list()
        for game in games:
            old_users += game.visited
        old_users = list(set(old_users))
        return old_users

    @property
    def sport_type(self):
        return self.gametype.sporttype_id

    @property
    def duration_beauty(self):
        duration = self.datetime_to - self.datetime
        seconds = duration.seconds
        if seconds % 3600 == 0:
            hours = int(seconds/3600)
            return formatters.show_hours(hours)
        else:
            seconds -= seconds % 60
            minutes = int(seconds/60)
            return formatters.show_minutes(minutes)

    @property
    def duration(self):
        return self.datetime_to - self.datetime

    def get_absolute_url(self):
        return "/game/%i" % self.id

    @property
    def near_time_status(self):
        event_date = timezone.localtime(self.datetime).date()
        now = timezone.localtime(timezone.now())
        today = now.date()
        tomorrow = today + datetime.timedelta(days=1)
        double_tomorrow = today + datetime.timedelta(days=2)
        if event_date == today and now < self.datetime:
            return 'Today'
        elif event_date == tomorrow:
            return 'Tomorrow'
        elif event_date == double_tomorrow:
            return 'After Tomorrow'
        else:
            return False

    @property
    def time_status(self):
        now = timezone.now()
        # считаем продоожительность события и высчитываем погрещнойсть для отображения статусов, аля "скоро начнется"
        if self.duration > datetime.timedelta(days=2):
            delta = datetime.timedelta(days=2)
        else:
            delta = self.duration
        # все возможные временные статусы события, влияющие на отображение
        if now <= self.datetime - delta:
            return 'WILL BE'
        elif now <= self.datetime:
            return 'COMING'
        elif now <= self.datetime_to:
            return 'IT GOES'
        else:
            return 'WAS'

    @property
    def subscribed(self):
        actions = UserGameAction.objects.filter(game=self).filter(action=UserGameAction.SUBSCRIBED)
        users = list()
        for action in actions:
            users.append(action.user)
        return users

    @property
    def reserved(self):
        actions = UserGameAction.objects.filter(game=self).filter(action=UserGameAction.RESERVED)
        users = list()
        for action in actions:
            users.append(action.user)
        return users

    @property
    def unsubscribed(self):
        actions1 = UserGameAction.objects.filter(game=self).filter(action=UserGameAction.UNSUBSCRIBED)
        actions2 = UserGameAction.objects.filter(game=self).filter(action=UserGameAction.UNRESERVED)
        users = list()
        for action in actions1:
            users.append(action.user)
        for action in actions2:
            users.append(action.user)
        return users

    @property
    def visited(self):
        actions = UserGameAction.objects.filter(game=self).filter(action=UserGameAction.VISITED)
        users = list()
        for action in actions:
            users.append(action.user)
        return users

    @property
    def notvisited(self):
        actions = UserGameAction.objects.filter(game=self).filter(action=UserGameAction.NOTVISITED)
        users = list()
        for action in actions:
            users.append(action.user)
        return users

    @property
    def notpay(self):
        actions = UserGameAction.objects.filter(game=self).filter(action=UserGameAction.NOTPAY)
        users = list()
        for action in actions:
            users.append(action.user)
        return users

    @property
    def has_place(self):
        if self.capacity == 0:
            return True
        actions = UserGameAction.objects.filter(game=self).filter(action=UserGameAction.SUBSCRIBED)
        count = actions.count()
        if count >= self.capacity:
            return False
        else:
            return True

    @property
    def has_reserved_place(self):
        actions = UserGameAction.objects.filter(game=self).filter(action=UserGameAction.RESERVED)
        count = actions.count()
        if count >= self.reserved_count:
            return False
        else:
            return True


# TODO: добавить условия, при которых возможно создание такого usergameaction'a
class UserGameAction(models.Model):
    class Meta():
        verbose_name = 'запись на игру'
        verbose_name_plural = 'записи на игру'
        app_label = 'games'
        unique_together = ("game", "user")

    SUBSCRIBED = 1
    UNSUBSCRIBED = 2
    RESERVED = 3
    UNRESERVED = 4
    VISITED = 5
    NOTVISITED = 6
    NOTPAY = 7
    ACTIONS = (
        (SUBSCRIBED, 'Записался'),
        (UNSUBSCRIBED, 'Отписался'),
        (RESERVED, 'В резерве'),
        (UNRESERVED, 'Вышел из резерва'),
        (VISITED, 'Посетил'),
        (NOTVISITED, 'Не пришел'),
        (NOTPAY, 'Не заплатил')
    )
    user = models.ForeignKey('users.User', verbose_name='Пользователь')
    game = models.ForeignKey(Game, verbose_name='Игра')
    datetime = models.DateTimeField(verbose_name='Дата действия', auto_now=True)
    action = models.PositiveSmallIntegerField(verbose_name='Действие', choices=ACTIONS)

    def __unicode__(self):
        return u'{} {} | {} | {}'.format(self.game.id, self.game, self.user, self.get_action_display())

    def text(self):
        return self.get_action_display()
