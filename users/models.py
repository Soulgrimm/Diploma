from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    phone = models.CharField(unique=True, default='+0 000 000 000', max_length=30, verbose_name='телефон')
    country = models.CharField(max_length=40, verbose_name='Страна', **NULLABLE)
    invite_code = models.CharField(unique=True, default='0000', max_length=6, verbose_name='инвайт-код')
    invited_by = models.ForeignKey('self', on_delete=models.RESTRICT, null=True, verbose_name='реферал')

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def invite_users(self):
        obj = User.objects.filter(invited_by=self.id)
        return obj
