from __future__ import absolute_import

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractUser):

    _STATUS_FINANCEIRO = (
        (0, 'Nenhum'),
        (1, 'Solicitante'),
        (2, 'Aprovador'),
        (3, 'Super'),
    )

    name = models.CharField(max_length=120, verbose_name=_("name"))
    email = models.CharField(max_length=120, unique=True,verbose_name=_("email"), blank=True, null=True)
    telefone = models.CharField(max_length=120,verbose_name=_("Telefone"), blank=True, null=True)
    username = models.CharField(max_length=120, unique=True, verbose_name=_("User Name"), blank=True, null=True)
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name=_("registration date"))
    data_nascimento = models.DateField(verbose_name="Data Nascimento", null=True, default=None)
    can_request = models.BooleanField(default=False, verbose_name="Pode Solicitar?")
    can_aprove = models.BooleanField(default=False, verbose_name="Pode Aprovar?")
    can_pay = models.BooleanField(default=False, verbose_name="Pode Repassar Recurso?")
    tp_user_financeiro = models.IntegerField(choices=_STATUS_FINANCEIRO, verbose_name="Tipo Usuario Financeiro", default=0)
    onesignal_id = models.CharField(max_length=120,verbose_name=_("ID OneSignal"), blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', ]

    class Meta:
        db_table = 'account'

    def __str__(self):
        return self.email

    def get_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        if self.username is None or self.username == "":
            self.username = self.email

        super(Account, self).save(*args, **kwargs)