
from django.contrib import admin
from django.urls import include, path
from django.http import * 
from django import *
from . import views,api

urlpatterns = [
    path('', views.pagina_inicio, name='pagina_inicio'),
    path('play-action',views.play_action, name="play-action"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/profile/", views.profile, name="profile"),
    path('cron/', views.pagina_inicio, name='index'),
    path('messages/', views.pagina_inicio, name='index'),
    path('ranking/', views.ranking, name='general_ranking'),
    path('ranking/<str:username>', views.ranking, name='profile_ranking'),
    path('register/', views.register, name='register'),
    path('actions/',views.actions, name="actions"),
    path('save_action',views.profileAjaxActions, name="save_action"),
    #API
    path('api/get_users',api.getUsers, name="getUsers"),
    path('get_user', api.get_user, name='get_user'),
    path('api/get_related_actions',api.getRelatedActions, name="getRelatedActions"),
    path('api/get_actions',api.getActions, name="get_actions"),
    path('api/get_userByUsername/<str:username>',api.getUsersByName, name="get_userByUsername")
]
