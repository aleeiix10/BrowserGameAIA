from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.writeLog, name='index'),
    path('cron/', views.index, name='index'),
    path('play-action', views.index, name='index'),
    path('messages/', views.index, name='index'),
    path('ranking/', views.index, name='index'),
]