from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserRols(models.Model):
    idUser= models.ForeignKey(User, on_delete=models.CASCADE)
    rold= models.IntegerField()

class Player(models.Model):
    name= models.ForeignKey(User, on_delete=models.CASCADE)
    level= models.IntegerField()
    life= models.IntegerField()
    energi= models.IntegerField()
    experience= models.IntegerField()


class GlobalOption(models.Model):
    opc= models.CharField(max_length=100)

class Accion(models.Model):
    user= models.ForeignKey(Player, on_delete=models.CASCADE)
    typeA= models.CharField(max_length=100)