from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db.models.fields import DateTimeField
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager




class Service(models.Model):
    """Администратор создает виды работ и их описание"""
    name = models.CharField(max_length=150, verbose_name= 'Вид работы')
    text = models.TextField(max_length=500, verbose_name= 'Описание')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name= 'Услуга'
        verbose_name_plural= 'Услуги'




class CustomUser(AbstractBaseUser, PermissionsMixin):
    """"USERNAME --- EMAIL полностью настраиваемая модель пользователя"""
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    phone_regex = RegexValidator(regex=r'^((\+7)+([0-9]){10})$', message=
    "ФОРМАТ дожен быть: +79998885555")
    phone = models.CharField(validators=[phone_regex], max_length=12,
                            verbose_name='Телефон',blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural= 'Пользователи'


class Work(models.Model):

    client_name = models.CharField(max_length=150, verbose_name= 'Покупатель')
    client_email = models.EmailField(verbose_name= 'Покупатель email')
    phone_regex = RegexValidator(regex=r'^((\+7)+([0-9]){10})$', message=
    "ФОРМАТ дожен быть: +79998885555")
    client_phone = models.CharField(validators=[phone_regex], max_length=12, verbose_name= 'Телефон покупателя') # validators should be a list
    work = models.ForeignKey (Service, on_delete = models.deletion.PROTECT, verbose_name= 'Вид работы', related_name="work")
    text = models.TextField(max_length=500, verbose_name= 'Описание')
    date = DateTimeField(auto_now_add=True,verbose_name= 'Дата оформления заказа')
    in_work = models.BooleanField(default=False, verbose_name= 'Заказ в работе')
    def __str__(self) :
        return "Заказ №" + str(self.id) + " - " + str(self.work)
    class Meta:
        verbose_name= 'Заказ'
        verbose_name_plural= 'Заказы'