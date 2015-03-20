# -*- coding: iso-8859-15 -*- 

from django.db import models

from datetime import datetime

from django.contrib.gis.db import models

from social.core.models import *

from django.core.files.storage import FileSystemStorage

from social.core.models import Social_node

#
#  Copyright (C) 2009 GSyC/LibreSoft
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
#    Author : Jorge Fernandez Gonzalez
#

class Manager(models.Model):
    user = models.ForeignKey(Person,null=False)
    events = models.ManyToManyField("Event",null=True)

class TeamMember(models.Model):
    user = models.ForeignKey(Person,null=False)
    team = models.ForeignKey("Team",null=False)
    event = models.ForeignKey("Event",null=False)

class Team(models.Model):
    group = models.ForeignKey(Group,null=False) # groupname unique (social.core.models)
    event = models.ManyToManyField("Event",null=False)
    responses = models.ManyToManyField("Response",null=True)

class Finished(models.Model):
    team = models.ForeignKey("Team",null=False)
    event = models.ForeignKey("Event",null=False)
    is_finished = models.BooleanField(null=False) # Indica si el equipo ha finalizado esta gymkhana

class AcquiredClue(models.Model):
    team = models.ForeignKey("Team",null=False)
    clue = models.ForeignKey("Clue",null=False)

class FirstChallenge(models.Model):
    event = models.ForeignKey("Event",null=False)
    team = models.ForeignKey("Team",null=False)
    first_challenge = models.ForeignKey("Challenge",null=True)

class Response(Social_node): # Almacena las respuestas que cada equipo dio a cada prueba
    challenge = models.ForeignKey("Challenge",null=False)
    response_text = models.CharField(max_length=255) #null=False
    is_correct = models.BooleanField(default=False)

    #position = models.PointField(srid=4326)
    #altitude = models.FloatField(help_text="In meters over the sea level", default=0.0)
    date = models.DateTimeField(default=datetime.now)

    photo = models.ImageField(upload_to="img", storage=FileSystemStorage())

    distance_difference = models.FloatField(default=-1)

class Clue(models.Model):
    challenge = models.ForeignKey("Challenge",null=False)
    number = models.IntegerField(null=False)
    help = models.CharField(max_length=255,null=False)
    cost = models.IntegerField(default=0,null=False)

class Challenge(models.Model):
    challenge = models.TextField(null=False)
    picture = models.ImageField(upload_to="img", storage=FileSystemStorage(),null=True)
    number = models.IntegerField(null=False)
    event = models.ForeignKey("Event",null=False)
    next_challenge_id = models.IntegerField(null=False)
    is_stop = models.BooleanField(default=False,null=False) # Indica si se necesita una respuesta correcta para poder continuar
    can_skip = models.BooleanField(default=False)
    max_score = models.IntegerField(default=100,null=False)
    challenge_type = models.IntegerField(default=1,null=False) # 1 -> Textual; 2 -> Photo; 3 -> Geolocation; ...
    augmented_reality = models.NullBooleanField(default=False,null=True) # Para las pruebas textuales, si hace uso del modulo de realidad aumentada
    target_place = models.PointField(srid=4326, null=True) # Si tipo = 3; punto geografico al que hay que llegar
    distance_to_target_place = models.FloatField(default=0.0,null=True)
    mark_place = models.NullBooleanField(default=False,null=True)
    objectives = models.ManyToManyField("LearningObjective", blank=True, null=True)

class Solution(models.Model):
    challenge = models.ForeignKey("Challenge",null=False)
    possible_solution = models.CharField(max_length=255,null=False)

class SkippedChallenge(models.Model):
    challenge = models.ForeignKey("Challenge",null=False)
    team = models.ForeignKey("Team",null=False)

class Scoreboard(models.Model):
    event = models.ForeignKey("Event",null=False)
    team = models.ForeignKey("Team",null=False)
    score = models.IntegerField(default=0,null=False)
    num_correct_responses = models.IntegerField(default=0,null=False)
    num_incorrect_responses = models.IntegerField(default=0,null=False)

class Event(models.Model):
    title = models.CharField(max_length=255,null=False)
    celebration = models.DateField(default=datetime.now(),null=False)
    place = models.CharField(max_length=255,null=False)
    welcome_text = models.TextField(null=False)
    goodbye_text = models.TextField(null=False)
    is_closed = models.BooleanField(default=True,null=False)
    language = models.CharField(max_length=255,null=True)
    configurate_teams = models.BooleanField(default=False,null=False) # True => manager will configure teams.
    image = models.ImageField(upload_to="img", storage=FileSystemStorage(), null=True)
    difficulty = models.IntegerField(default=3)
    score = models.IntegerField(default=0)
    objectives = models.ManyToManyField("LearningObjective", blank=True, null=True, related_name="learning_objectives")

class LearningObjective(models.Model):
    objective = models.CharField(max_length=255,null=False)

class Message(Social_node):
    event = models.ForeignKey("Event",null=False)
    from_manager = models.ForeignKey("Manager",blank=True,null=True,related_name="sender_manager")
    from_team = models.ForeignKey("Team",blank=True,null=True,related_name="sender_team")
    to_manager = models.ForeignKey("Manager",blank=True,null=True,related_name="receiver_manager")
    to_team = models.ManyToManyField("Team",blank=True,null=True,related_name="receiver_team")
    text = models.TextField(null=False)

    #position = models.PointField(srid=4326, null=True)
    #altitude = models.FloatField(help_text="In meters over the sea level", default=0.0, null=True)
    date = models.DateTimeField(default=datetime.now)

class Parameters(models.Model):
    event_id = models.IntegerField(null=False)
    team_id = models.IntegerField(null=False)
    time = models.DateTimeField(null=False)
    length = models.IntegerField(null=False)
