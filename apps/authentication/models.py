from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-
    updating ``created`` and ``modified`` fields.
    """
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name="Дата создания")
    modified = models.DateTimeField(auto_now=True,
                                    verbose_name="Дата изменения")

    class Meta:
        abstract = True


class Role(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"

    def __str__(self):
        return f"{self.name}"


class City(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

    def __str__(self):
        return f"{self.name}"


class Country(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return f"{self.name}"


class Company(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.ForeignKey(City,
                             related_name='companies',
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True)
    country = models.ForeignKey(Country,
                                related_name='companies',
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)
    staff = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"

    def __str__(self):
        return f"{self.name}"


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password,
                     **extra_fields):
        """
        Create and save a User with given email, and password.
        """
        if not email:
            raise ValueError('The given username must be set')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser, TimeStampedModel):
    role = models.ForeignKey(Role,
                             related_name='users',
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True)
    first_name = models.CharField(max_length=128, null=True,blank=True)
    last_name = models.CharField(max_length=128, null=True,blank=True)
    company = models.ForeignKey(Company,
                                related_name='users',
                                on_delete=models.CASCADE,
                                null=True,
                                blank=True)

    class Mets:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
