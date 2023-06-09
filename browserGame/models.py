from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    level = models.IntegerField(default=1)
    current_life = models.IntegerField(default=10)
    current_mana = models.IntegerField(default=10)
    experience = models.IntegerField(default=0)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='browsergame_users_groups',  # nuevo nombre de acceso inverso
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='browsergame_users_permissions',  # nuevo nombre de acceso inverso
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
        related_query_name='browsergame_user',
    )

class GlobalOption(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    last_updated_cron= models.DateTimeField()
    time_cron_execute_seconds = models.IntegerField()

class Action(models.Model):
    categories = [
        ('A', 'Agressiva'),
        ('D', 'Defensiva'),
        ('N', 'Neutra'),
    ]
    name= models.CharField(max_length=50)
    category= models.CharField(max_length=1, choices=categories)
    cost= models.IntegerField()
    succesPercentage= models.IntegerField()
    points= models.IntegerField()
    def __str__(self):
        return self.name

class Event(models.Model):
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)
    user_attacked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_attacked', blank=True, null=True)
    class Meta:
        ordering = ['-timestamp']

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
    created_at = models.DateTimeField(auto_now_add=False)

    class Meta:
        ordering = ['-created_at'] #POSIBLE CAMBIO, AÑADIRLO EN EL ADMIN.py
