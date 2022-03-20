from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db.models.fields import DateTimeField
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """"USERNAME --- EMAIL полностью настраиваемая модель пользователя"""
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    phone_regex = RegexValidator(regex=r'^((\+7)+([0-9]){10})$', message=
    "ФОРМАТ дожен быть: +79998885555")
    phone = models.CharField(validators=[phone_regex], verbose_name='Телефон',
                             max_length=12, blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class WorkType(models.Model):
    type = models.CharField(max_length=300, verbose_name='Вид работы')

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Вид работы'
        verbose_name_plural = 'Виды работ'


class Firm(models.Model):
    """Зарегистрированный пользователь может создать фирму"""
    owner = models.ForeignKey(CustomUser, on_delete=models.deletion.CASCADE,
                              verbose_name='Владелец', related_name="customUser")
    name = models.CharField(max_length=300, verbose_name='Название фирмы')
    date = DateTimeField(auto_now_add=True, verbose_name='Дата регистрации фирмы')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Фирма'
        verbose_name_plural = 'Фирмы'

class Service(models.Model):
    """ФИРМА добавляет услуги"""
    firm = models.ForeignKey(Firm, on_delete=models.deletion.CASCADE,
                             verbose_name='Фирма', related_name="firm")
    workType = models.ForeignKey(WorkType, on_delete=models.deletion.CASCADE,
                                 verbose_name='Вид работ', related_name="work")
    content = models.TextField(max_length=1000, verbose_name='Описание')
    price = models.IntegerField( verbose_name='Цена')

    def __str__(self):
        return self.workType.type

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class Order(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.deletion.CASCADE,
                              verbose_name='Клиент', related_name="client")
    workType = models.ManyToManyField(WorkType, verbose_name='Вид работ', related_name="workType")
    description = models.TextField(max_length=500, verbose_name='Описание заказа')
    date = DateTimeField(auto_now_add=True, verbose_name='Дата оформления заказа')
    in_work = models.BooleanField(default=False, verbose_name='Заказ в работе')
    is_done = models.BooleanField(default=False, verbose_name='Заказ в выполнен')

    def __str__(self):
        return "Заказ №" + str(self.pk)


    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderInWork(models.Model):
    order = models.OneToOneField(Order, on_delete=models.PROTECT, verbose_name='Заказ', related_name="order")
    executor = models.ForeignKey(Firm, on_delete=models.PROTECT, verbose_name='Фирма-исполнитель',
                                 related_name="firmExecutor")
    date = DateTimeField(auto_now_add=True, verbose_name='Принято к исполнению')

    def __str__(self):
        return str(self.order)

    def save(self, *args, **kwargs):
        # self.order.in_work = True
        super().save(*args, **kwargs)  # Call the "real" save() method.
        order = Order.objects.get(id=self.order_id)
        order.in_work = True
        order.save()

    class Meta:
        verbose_name = 'Заказ в работе'
        verbose_name_plural = 'Заказы в работе'
        ordering = ['-date']




class OrderInDone(models.Model):
    # objects = NaRabotuManager()  # Забирает только отсортированные Менеджером объекты!!!
    order = models.OneToOneField(Order, on_delete=models.PROTECT, verbose_name='Заказ', related_name="done_order")
    executor = models.ForeignKey(Firm, on_delete=models.PROTECT, verbose_name='Фирма-исполнитель',
                                 related_name="done_firmExecutor")
    date = DateTimeField(auto_now_add=True, verbose_name='Заказ выполнен')

    def __str__(self):
        return str(self.order)

    def save(self, *args, **kwargs):
        # self.order.in_work = True
        super().save(*args, **kwargs)  # Call the "real" save() method.
        order = Order.objects.get(id=self.order_id)
        orderInWork = OrderInWork.objects.get(order_id=self.order_id)
        # orderInWork1 = OrderInWork.objects.all()
        order.in_work = False
        order.is_done = True
        print(orderInWork)
        # print(orderInWork1[0].__dict__)
        orderInWork.delete()
        order.save()

    class Meta:
        verbose_name = 'Выполненый заказ'
        verbose_name_plural = 'Выполненные заказы'
        ordering = ['-date']