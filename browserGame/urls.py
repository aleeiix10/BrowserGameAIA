
from django.contrib import admin
from django.urls import include, path
from django.http import * 
from django import *
from . import views

urlpatterns = [
    path('', views.pagina_inicio, name='pagina_inicio'),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/profile/", views.profile, name="profile"),
    path('cron/', views.pagina_inicio, name='index'),
    path('play-action', views.play_action, name='play_action'),
    path('messages/', views.pagina_inicio, name='index'),
    path('ranking/', views.pagina_inicio, name='index'),
    path('register/', views.register, name='register'),
]
