# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    path('', views.index, name='home'),
    path('profile/', views.profile, name='profile'),
    path('client/', views.zakaz_create, name='create-zakaz'),
    path('client/zakaz/', views.StudentListView.as_view(), name='list-zakaz'),
    path('client/company/', views.create_Company, name='create-company'),
    path('create-user/', views.userAdd, name='create-user'),
    path('client/zakaz-check/<int:pk>/', views.StudentDetailView.as_view(), name='check-zakaz'),
    path('accept-zakaz/<int:pk>/', views.accept_zakaz, name='accept'),
    path('verify-zakaz/<int:pk>/', views.verify_zakaz, name='verify'),
    path('send-zakaz/<int:pk>/', views.send_zakaz, name='send'),
    # Matches any html file

    path('clients/', views.clients, name='admin-clients'),
    path('list-tovar/', views.list_tovar, name='list-tovar'),
    path('zakaz/', views.TeacherListView.as_view(), name='update-zakaz'),
    path('delete-zakaz/<int:pk>/', views.zakazDelete, name='delete-zakaz'),
    path('delete-company/<int:pk>/', views.companyDelete, name='delete-company'),

    re_path(r'^.*\.*', views.pages, name='pages'),



]
