
from django.contrib import admin
from django.urls import include, path
from django.http import * 
from django import *
from . import views,api

urlpatterns = [
    path('', views.pagina_inicio, name='pagina_inicio'),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/profile/", views.profile, name="profile"),
    path('cron/', views.pagina_inicio, name='index'),
    path('messages/', views.pagina_inicio, name='index'),
    path('ranking/', views.pagina_inicio, name='index'),
    path('register/', views.register, name='register'),
    path('api/get_users',api.getUsers, name="getUsersId"),

]
