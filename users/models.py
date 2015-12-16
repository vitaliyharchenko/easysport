# coding=utf-8
import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.utils import timezone
from utils.fields import PhoneField
from utils.formatters import age_format
from sports.models import Amplua
from places.models import City


class UserManager(BaseUserManager):
    def create_user(self, email, password, is_superuser, is_staff, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('Users must have an email address')
        is_active = extra_fields.pop("is_active", True)
        is_responsible = extra_fields.pop("is_responsible", False)
        is_admin = extra_fields.pop("is_admin", False)
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
    is_active = models.BooleanField(u'Активность', default=True,
                                    help_text="Вместо удаления аккаунта, сделайте его неактивным")
    is_referee = models.BooleanField('Судья', default=False,
                                     help_text="Может судить игры")
    is_coach = models.BooleanField('Тренер', default=False,
                                   help_text="Может вести тренеровки")
    is_responsible = models.BooleanField('Ответственный', default=False,
                                         help_text="Заполняет отчеты, редактирует игры")
    is_organizer = models.BooleanField('Организатор', default=False,
                                       help_text="Создает игры, площадки, назначает ответственных")
    is_admin = models.BooleanField('Админ', default=False,
                                   help_text="Назначает организаторов, работает с зарплатами и базами данных")
    is_staff = models.BooleanField('Редактор', default=False,
                                   help_text="Определяет, может ли пользователь войти в админку")

    banned = models.BooleanField('Забанен', default=False,
                                 help_text="Банит пользователя")

    city = models.ForeignKey(City, blank=True, null=True, verbose_name='Город')
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True, verbose_name='Аватар')
    date_joined = models.DateTimeField('Дата регистрации', default=timezone.now)
    bdate = models.DateField('Дата рождения', auto_now_add=False, blank=True, null=True)
    first_name = models.CharField(u'Имя', max_length=120)
    last_name = models.CharField(u'Фамилия', max_length=120)
    vkuserid = models.IntegerField(unique=True, null=True, blank=True)
    sex = models.CharField(max_length=1, choices=(('m', 'мужской'), ('f', 'женский')), verbose_name='Пол')
    phone = PhoneField(verbose_name='Телефон', blank=True)
    amplua = models.ForeignKey(Amplua, verbose_name=u'Амплуа', blank=True, null=True)
    weight = models.PositiveSmallIntegerField(default=0, verbose_name='Вес')
    height = models.PositiveSmallIntegerField(default=0, verbose_name='Рост')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    REGISTRATION_FIELDS = ['avatar'] + ['first_name', 'last_name', 'city'] + ['sex'] + ['city'] + ['bdate'] + ['phone'] + [USERNAME_FIELD]

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'
        db_table = 'auth_user'
        abstract = True

    def get_full_name(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.last_name

    def get_beautiful_phone(self):
        phone = self.phone.__str__()
        return phone[:2] + ' (' + phone[2:5] + ') ' + phone[5:8] + '-' + phone[8:10] + '-' + phone[10:12]

    @property
    def age(self):
        today = datetime.date.today()
        return today.year - self.bdate.year - ((today.month, today.day) < (self.bdate.month, self.bdate.day))

    def beautiful_age(self):
        return age_format(self.age)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_absolute_url(self):
        return "/users/%i" % self.id

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