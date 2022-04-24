# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import CustomUser, Role, Company,City,Country
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Role)
admin.site.register(Company)
admin.site.register(City)
admin.site.register(Country)