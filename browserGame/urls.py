
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
]