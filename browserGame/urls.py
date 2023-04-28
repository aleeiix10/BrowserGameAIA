from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.pagina_inicio, name='pagina_inicio'),
    path('register/', views.register, name='register'),
    path("accounts/", include("django.contrib.auth.urls")),
]