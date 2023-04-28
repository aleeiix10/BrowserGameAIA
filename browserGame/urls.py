
from django.contrib import admin
from django.urls import include, path
from django.http import * 
from django import *
from . import views

urlpatterns = [
    path('', views.pagina_inicio, name='pagina_inicio'),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/profile/", views.profile, name="profile"),
    path("email/",views.enviar_email,name='enviar_email'),
    path('index/', views.index, name='index'),
    path('cron/', views.index, name='index'),
    path('play-action', views.index, name='index'),
    path('messages/', views.index, name='index'),
    path('ranking/', views.index, name='index'),
]