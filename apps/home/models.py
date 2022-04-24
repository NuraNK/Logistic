# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from apps.authentication.models import CustomUser
from apps.authentication.models import Company


class Tovar(models.Model):
    name = models.CharField(max_length=128)
    price = models.IntegerField()

    def __str__(self):
        return self.name

class Sklad(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    obiem = models.IntegerField(default=100, verbose_name="Обьем в литрах")
    tovar = models.ForeignKey(
        Tovar,
        on_delete=models.CASCADE,
        verbose_name="Тип Товара"
    )
    STATUS = (
        ("Ожидается", "Ожидается"),
        ("Принято", "Принято"),
        ("В_пути", "В_пути"),
        ("Доставлено", "Доставлено"),
    )
    status = models.CharField(choices=STATUS, max_length=128)
    date = models.DateTimeField(auto_now=True)
    accept = models.CharField(max_length=128, default='')

    def price_check(self):
        return int(self.obiem)*int(self.tovar.price)

    def __str__(self):
        return f'{self.company} - {self.tovar}'

