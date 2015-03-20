from django.db import models
from datetime import datetime
from django.contrib.gis.db import models
from social.core.models import *
from social.core.models import Social_node
# Create your models here.

class Group(models.Model):
    manager=models.ManyToManyField("Player",null=True)
    name=models.TextField(null=False)
    private=models.BooleanField(null=False)
    description=models.TextField(null=False)
    
class Player(models.Model):
    person = models.ForeignKey(Person,null=False)
    is_superuser = models.BooleanField(null=False)
    is_manager = models.BooleanField(null=False)
    is_player = models.BooleanField(null=False)
    active_superuser = models.BooleanField(null=False)
    active_manager = models.BooleanField(null=False)
    active_player = models.BooleanField(null=False)
    groups=models.ManyToManyField(Group,null=True)
    
class Petition(models.Model):
    player=models.ForeignKey(Player, null=False)
    for_super=models.BooleanField(null=False)
    for_manager=models.BooleanField(null=False)
    date=models.DateTimeField(null=False)
    
class PetitionGroup(models.Model):
    player=models.ForeignKey(Player,null=False)
    group=models.ForeignKey(Group, null=False)
    date=models.DateTimeField(null=False)

class SystemMessage(models.Model):
    to=models.ManyToManyField(Player,null=True)
    message=models.TextField(null=False)
    date=models.DateTimeField(null=False)
    
class Event(models.Model):
    group=models.ManyToManyField(Group, null=True)
    name=models.TextField(null=False)
    description=models.TextField(null=False)
    active=models.BooleanField(null=False)
    manager=models.ForeignKey(Player,null=False)
    qr=models.BooleanField(null=False)
    date=models.DateTimeField(null=False)
    attemps=models.IntegerField(null=False)
    
class Question(models.Model):
    event=models.ForeignKey(Event, null=False)
    text=models.TextField(null=False)
    level=models.IntegerField(null=False)
    qr=models.BooleanField(null=False)
    
class Answer(models.Model):
    question=models.ForeignKey(Question, null=False)
    text=models.TextField(null=False)
    next=models.IntegerField(null=True)
    message=models.TextField(null=False)
    
class Challenge(models.Model):
    event=models.ForeignKey(Event,null=False)
    user=models.ForeignKey(Player,null=False)
    date=models.DateTimeField(default=datetime.now(),null=False)
    date_finish=models.DateTimeField(null=True)
    finish=models.BooleanField(null=False)
    phone=models.BooleanField(null=False)
    cancel=models.BooleanField(null=False)
class Responses(models.Model):
    challenge=models.ForeignKey(Challenge,null=False)
    question=models.ForeignKey(Question,null=False)
    date=models.DateTimeField(default=datetime.now())
    answer=models.ForeignKey(Answer,null=False)
    latitude=models.FloatField(null=True)
    longitude=models.FloatField(null=True)


