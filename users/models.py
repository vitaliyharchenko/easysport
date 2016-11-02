# coding=utf-8
import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.utils import timezone
from utils.fields import PhoneField
from sports.models import Amplua
from places.models import City
from games.models import UserGameAction, Game


class UserManager(BaseUserManager):
    def create_user(self, email, password, is_superuser=False, is_active=False, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('Users must have an email address')

        is_staff = is_superuser
        is_admin = extra_fields.pop("is_admin", False)
        is_responsible = extra_fields.pop("is_responsible", False)
        first_name = extra_fields.pop("first_name", '')
        last_name = extra_fields.pop("last_name", '')

        user = self.model(
            email=self.normalize_email(email),
            is_active=is_active,
            is_responsible=is_responsible,
            is_staff=is_staff,
            is_admin=is_admin,
            is_superuser=is_superuser,
            first_name=first_name,
            last_name=last_name,
            last_login=now,
            date_joined=now,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        return self.create_user(email, password, True, True, **extra_fields)


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Email', max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(u'Активность', default=False,
                                    help_text="Вместо удаления аккаунта, сделайте его неактивным")
    is_referee = models.BooleanField('Судья', default=False,
                                     help_text="Может судить игры")
    is_coach = models.BooleanField('Тренер', default=False,
                                   help_text="Может вести тренеровки")
    is_responsible = models.BooleanField('Ответственный', default=False,
                                         help_text="Заполняет отчеты, редактирует игры")
    is_organizer = models.BooleanField('Организатор', default=False,
                                       help_text="Создает игры, назначает ответственных")
    is_admin = models.BooleanField('Админ', default=False,
                                   help_text="Работает с пользователями, площадками и финансами")
    is_staff = models.BooleanField('Редактор', default=False,
                                   help_text="Определяет, может ли пользователь войти в админку")

    banned = models.BooleanField('Забанен', default=False,
                                 help_text="Сделать активным для бана")

    city = models.ForeignKey(City, blank=True, null=True, verbose_name='Город')
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True, verbose_name='Аватар')
    date_joined = models.DateTimeField('Дата регистрации', default=timezone.now)
    bdate = models.DateField('Дата рождения', auto_now_add=False, blank=True, null=True)
    first_name = models.CharField(u'Имя', max_length=120)
    last_name = models.CharField(u'Фамилия', max_length=120)
    vkuserid = models.BigIntegerField(unique=True, null=True, blank=True)
    fbuserid = models.BigIntegerField(unique=True, null=True, blank=True)
    sex = models.CharField(max_length=1, choices=(('m', 'мужской'), ('f', 'женский')), verbose_name='Пол')
    phone = PhoneField(verbose_name='Телефон', blank=True, null=True, unique=True)
    amplua = models.ForeignKey(Amplua, verbose_name=u'Амплуа', blank=True, null=True)
    weight = models.PositiveSmallIntegerField(default=0, verbose_name='Вес')
    height = models.PositiveSmallIntegerField(default=0, verbose_name='Рост')

    referer = models.ForeignKey('users.User', blank=True, null=True, verbose_name='Кем приглашен')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    REGISTRATION_FIELDS = ['avatar'] + ['first_name', 'last_name', 'city'] + ['sex'] + ['city'] + ['bdate'] + ['phone'] + [USERNAME_FIELD]

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'
        db_table = 'auth_user'
        abstract = True

    def save(self, *args, **kwargs):
        if self.is_admin or self.is_organizer or self.is_responsible:
            self.is_staff = True
        else:
            self.is_staff = False
        super(AbstractUser, self).save(*args, **kwargs)

    def get_full_name(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.last_name

    @property
    def age(self):
        today = datetime.date.today()
        return today.year - self.bdate.year - ((today.month, today.day) < (self.bdate.month, self.bdate.day))

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_absolute_url(self):
        return "/users/%i" % self.id

    @property
    def gamesvisited(self):
        games_ids = UserGameAction.objects.filter(user=self, action=UserGameAction.VISITED).values_list('game', flat=True)
        return Game.objects.filter(pk__in=games_ids).order_by('-datetime')[:10]

    @property
    def gamesnotvisited(self):
        games_ids = UserGameAction.objects.filter(user=self, action=UserGameAction.NOTVISITED).values_list('game', flat=True)
        return Game.objects.filter(pk__in=games_ids).order_by('-datetime')[:10]

    @property
    def gamesnotpay(self):
        games_ids = UserGameAction.objects.filter(user=self, action=UserGameAction.NOTPAY).values_list('game', flat=True)
        return Game.objects.filter(pk__in=games_ids).order_by('-datetime')[:10]

    def __str__(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    def __unicode__(self):
        return u'{} {}'.format(self.first_name, self.last_name)


class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        app_label = 'users'

    def get_absolute_url(self):
        return "/user/%i" % self.id


class UserActivation(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=100, blank=True)
    request_time = models.DateTimeField(default=timezone.now)
    confirm_time = models.DateTimeField('Дата активации', blank=True, null=True)

    def __str__(self):
        return self.user.email

    def __unicode__(self):
        return self.user.email

    class Meta:
        verbose_name_plural = u'Активации'