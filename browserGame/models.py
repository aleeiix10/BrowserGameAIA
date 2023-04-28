from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.
# class UserGame(AbstractUser):
#     level = models.IntegerField(default=1)
#     max_life = models.IntegerField(default=10)
#     max_mana = models.IntegerField(default=10)
#     experience = models.IntegerField(default=0)

class UserRol(models.Model):
    rols= [
        (0,"user"),
        (1,"admin"),
    ]
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    rol= models.IntegerField(choices=rols, default=0)

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    #name= models.ForeignKey(User, on_delete=models.CASCADE)
    current_life = models.IntegerField(default=10)
    current_mana = models.IntegerField(default=10)

class GlobalOption(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

class Action(models.Model):
    categories = [
        ('A', 'Agressiva'),
        ('D', 'Defensiva'),
        ('N', 'Neutra'),
    ]
    name= models.CharField(max_length=10)
    category= models.CharField(max_length=1, choices=categories)
    cost= models.IntegerField()
    succesPercentage= models.IntegerField()
    points= models.IntegerField()

class Event(models.Model):
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)

class Log(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    typeOfLog= [
        ("I","Info"),
        ('W',"Warging"),
        ('E',"Error"),
        ("F","Fatal")
    ]
    typeLog= models.CharField(max_length=1, choices=typeOfLog)
    message= models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']