from django.db import models

# Create your models here.
from django.contrib.auth.models import User

# Create your models here.
class userRols(models.Model):
    idUser= models.ForeignKey(User, on_delete=models.CASCADE)
    rold= models.IntegerField()

class players(models.Model):
    # name= models.ForeignKey(User.objects.filter["name":name], on_delete=models.CASCADE)
    level= models.IntegerField()
    life= models.IntegerField()
    energi= models.IntegerField()
    experience= models.IntegerField()


class globalOptions(models.Model):
    opc= models.CharField(max_length=100)

class accions():
    user= models.ForeignKey(players, on_delete=models.CASCADE)
    typeA= models.CharField(max_length=100)