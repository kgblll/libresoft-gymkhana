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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>._
# 
#    Author : Jorge Fernandez Gonzalez <jorge.fernandez.gonzalez __at__ gmail.com>
#

from apps.gymkhana.models import *

import StringIO
import random

import os
# Django settings for server project.
import sys
from os.path import abspath, dirname, join
from os import path
from PIL import Image

from apps.gymkhana.urls import BASEDIR

LEVEL = [ ['Beginner', 0], ['Amateur', 10000], ['Advanced', 25000], ['Professional', 50000], ['Boss', 100000], ['Major', 500000], ['Master', 1000000] ]
#LEVEL = [ ['Beginner', 0], ['Amateur', 350], ['Advanced', 750], ['Professional', 1450], ['Boss', 1900], ['Major', 2000], ['Master', 2050] ]

TEXTUAL_CHALLENGE	= 1
PHOTO_CHALLENGE		= 2
GEOLOCATION_CHALLENGE	= 3

def get_event(event_id):
    try:
      event = Event.objects.get(id=event_id)
      return True, event
    except:
      return False, "Invalid Event."

def get_user(user_id):
    try:
      users = Person.objects.all().order_by('id')
      for user in users:
        if user.id == int(user_id):
          return True, user
      return False, "Invalid User."
    except:
      return False, "Invalid User."

def get_challenge(event, challenge_id):
    try:
      challenge = event.challenge_set.get(id=challenge_id)
      return True, challenge
    except:
      return False, "Invalid Challenge."

def get_team(event, team_id):
    try:
      team = event.team_set.get(id=team_id)      
      return True, team
    except:
      return False, "Invalid Team."

def get_team_by_name(event, team_name):
    try:
      group = Group.objects.get(name=team_name)
      team = event.team_set.get(group=group)
      return True, team
    except:
      return False, "Invalid Team."

def get_team_by_id(team_id):
    try:
      team = Team.objects.get(id=team_id)
      return True, team
    except:
      return False, "Invalid Team."

def get_team_member(team, team_member_id):
    try:
      team_member = team.teammember_set.get(id=team_member_id)
      return True, team_member
    except:
      return False, "Invalid Team Member."

def get_team_member_by_user_id(event, user_id):
    try:
      person = Person.objects.get(id=user_id)
      try:
        team_member = TeamMember.objects.get(event=event, user=person.id)
      except:
        return True, None
      return True, team_member
    except:
      return False, "Invalid TeamMember."

def get_list_team_members():
    try:
      #person = Person.objects.get(id=user_id)
      #try:
      #  print "4bis"
      #team_members = TeamMember.objects.get(user=person.id)
      team_members = TeamMember.objects.all()
      #  print "5bis"
      #except:
      #  print "6bis"
      #  return True, None
      return True, team_members
    except:
      return True, None

def check_format(request, DEFAULT_FORMAT):
    if "format" in request.GET:
      format = request.GET["format"].lower().strip()
    elif "format" in request.POST:
      format = request.POST["format"].lower().strip()
    else:
      format = DEFAULT_FORMAT
      #return False, "Missing \"format\" Parameter."

    if format == 'xml':
      return True, 'xml'
    elif format == 'json':
      return True, 'json'
    elif format == 'html':
      return True, 'html'
    else:
      return False, "Invalid Format. Only .xml, .json and .html ."

def check_logged_user(request):
    if "_auth_user_id" in request.session:
      try:
        if type(Person.objects.get(id=request.session["_auth_user_id"])) == Person:
          return True
      except:
        pass
    return False

def check_session_user_type(request):
    try:
      user_id = request.session["_auth_user_id"]
      user = Person.objects.get(id=user_id)
      if type(Manager.objects.get(user=user)) == Manager:
        isAdmin = True
    except:
      isAdmin = False
    return isAdmin

def check_user_type(user):
    try:
      if type(Manager.objects.get(user=user)) == Manager:
        isAdmin = True
    except:
      isAdmin = False
    return isAdmin

def create_scoreboard(event, team):
    try:
      scoreboard = Scoreboard.objects.get(event=event,team=team)
      scoreboard.score = 0
      scoreboard.num_correct_responses = 0
      scoreboard.num_incorrect_responses = 0
    except:
      scoreboard = Scoreboard(event=event,team=team,score=0,num_correct_responses=0,num_incorrect_responses=0)
    scoreboard.save()

def get_manager_by_id(event, manager_id):
    try:
      manager = Manager.objects.get(id=manager_id)
    except:
      return False, "Invalid Manager."
    events = manager.events.all()
    success = 0
    for aux_event in events:
      if event == aux_event and success == 0:
        success = 1
    if success == 1:
      return True, manager
    else:
      return False, "Invalid Manager."

def get_manager(event):
    try:
      managers = Manager.objects.all()
      result = None
      for manager in managers:
        try:
          events = manager.events.all()
          for aux_event in events:
            if event == aux_event:
              result = manager
        except:
          pass
      if result != None:
        return True, result
      else:
        return False, "Invalid Event_Manager."
    except:
      return False, "Invalid Event_Manager."

def get_message(event, message_id):
    try:
      message = event.message_set.get(id=message_id)      
      return True, message
    except:
      return False, "Invalid Message."

def get_information_gymkhana(event, team, information_type):
    if information_type == "start_gymkhana":
      text = event.welcome_text
      return True, "ok", text, None
    elif information_type == "finish_gymkhana":
      text = event.goodbye_text
      team.finished = True
      team.save()
      scoreboard = Scoreboard.objects.get(event=event,team=team)
      return True, "ok", text, scoreboard
    else:
      error_message = "Incorrect Parameter \'information\' Value."
      return False, error_message, None, None

def search_following_challenge(event, challenge, team, message):
    first_challenge = FirstChallenge.objects.get(event=event,team=team)
    if message == "Continue" and ( (challenge.next_challenge_id == first_challenge.first_challenge.id) or (challenge.next_challenge_id == int(-1)) ): # si he recorrido la lista entera de pruebas, he acabado.
      try:
        # Si la prueba que ahora ha respondido bien, habia sido saltada, la borro de la DB para evitar problemas futuros
        skipped_challenge = SkippedChallenge.objects.get(challenge=challenge,team=team)
        responses = team.responses.filter(challenge=challenge)
        for response in responses:
          if response.is_correct == True or (response.is_correct == False and response.challenge.is_stop == False):
            skiped_challenge.delete()
      except:
        pass
      
      skipped_challenges = SkippedChallenge.objects.filter(team=team).order_by("id")
      count = 0
      for i in range(len(skipped_challenges)):
        if skipped_challenges[i].challenge.event == event:
          count = count + 1
      if count > 0:
        found = 0
        for i in range(len(skipped_challenges)):
          if found == 0 and skipped_challenges[i].challenge.event == event:
            next_challenge_id = skipped_challenges[i].challenge.id
            is_last_challenge = "False"
            found = 1
      else:
        is_last_challenge = "True"
        next_challenge_id = -1
    elif message == "Repeat":
      is_last_challenge = "False"
      next_challenge_id = challenge.id
    else: # si se puede continuar y no es la ultima prueba de la gymkhana:
      # Aqui ahora, ante una respuesta correcta, lo que hay que ver es si la next_challenge_id ya esta contestada correctamente o
      # si tenemos que ir saltando...
      try:
        # Si la prueba que ahora ha respondido bien, habia sido saltada, la borro de la DB para evitar problemas futuros
        skipped_challenge = SkippedChallenge.objects.get(challenge=challenge,team=team)
        responses = team.responses.filter(challenge=challenge)
        for response in responses:
          if response.is_correct == True or (response.is_correct == False and response.challenge.is_stop == False):
            skipped_challenge.delete()
      except:
        pass

      challenges = event.challenge_set.all().order_by("number")
      responses = team.responses.all()
      next_challenge = Challenge.objects.get(id=challenge.next_challenge_id)
      success = 0
      while success == 0 and next_challenge != challenge:
        for response in responses:
          if response.challenge == next_challenge and (response.is_correct == True or (response.is_correct == False and response.challenge.is_stop == False)) and success == 0:
            success = 1
        if success == 1: # Si he encontrado que la prueba que intento como proxima, ya esta respondida correctamente, tengo que seguir analizando
          success = 0
          next_challenge = Challenge.objects.get(id=next_challenge.next_challenge_id)
        else: # Si no he encontrado una respuesta valida para la prueba que he analizado, entonces esa es la siguiente de la gymkhana.
          success = 1

      found = 0
      if challenge == next_challenge:
        responses = team.responses.all()
        for response in responses:
          if response.challenge == challenge and (response.is_correct == True or (response.is_correct == False and response.challenge.is_stop == False)):
            is_last_challenge = "True"
            next_challenge_id = -1
            found = 1
        if found == 0:
          next_challenge_id = next_challenge.id
          is_last_challenge = "False"
      else:
        next_challenge_id = next_challenge.id
        is_last_challenge = "False"

    return is_last_challenge, next_challenge_id

def read_photo(request):
    # Recogemos el fichero que el usuario nos ha mandado como su foto
    # (segun la documentacion de Django, el mismo se encarga de comprobar
    # que se trata de una imagen -> modelo ImageField):
    if 'photo' in request.FILES:
      try:
        # ImageField del modelo de Django ya comprueba que sea una imagen valida.
        # De todos modos metemos un numero aleatorio por si el nombre de la foto
        # de dos o mas usuarios distintos coincidiera, y ademas porque no podemos
        # fiarnos de lo que el usuario introduzca (/etc/, /dev/, /root/ por ejemplo):
        if 'filename' in request.POST:
          filename = '%s_%s' % (random.randint(1,10000000000000), request.POST["filename"].strip())
        else:
          filename = 'manager_%s_%s' % (random.randint(1,10000000000000), request.FILES["photo"])
        photo = Image.open(request.FILES['photo'])
        photo.save('%s%s' % (BASEDIR + "/img/", filename))
      except IOError:
        return False, "The image is incorrect."
      return True, filename
    else:
      return False, "Missing \'photo\' Parameter in POST Petition."

def get_current_challenge(event, team):
    #proofs = event.proof_set.all().order_by('number')
    responses = team.responses.all()
    first_challenge = FirstChallenge.objects.get(event=event, team=team)
    first_challenge_id = first_challenge.first_challenge.id
    challenge = first_challenge.first_challenge

    found = 0
    num_iterations = 0
    while found == 0:
      passed = 0
      #responses_to_proof = 0
      for response in responses:
        if passed == 0:
         if response.challenge == challenge:
           #responses_to_proof = 1
           if challenge.is_stop and response.is_correct:
             passed = 1
             #found = 1
             #current_proof = proof
           elif not challenge.is_stop:
             passed = 1
      if passed == 0: # En caso de que no haya ninguna respuesta a esta prueba, me la quedo #responses_to_proof == 0 or
        found = 1
        current_challenge = challenge
      else:
        #if num_iterations == 0:
        next_challenge_id = challenge.next_challenge_id
        if next_challenge_id != first_challenge_id: #and num_iterations == 0:
          challenge = Challenge.objects.get(id=next_challenge_id)
          num_iterations = num_iterations + 1
        else: # Si el id de prueba a intentar ahora, coincide con el de la first_challenge de la gymkhana para ese equipo,
              # quiere decir que ya he recorrido todas las pruebas y por tanto no queda ninguna por resolver.
          found = 1
          current_challenge = None

    return True, "ok", current_challenge

def get_overall_standings(many):
    correct, team_members = get_list_team_members()
    users = []
    points = []
    num_events = []
    for team_member in team_members:
      try:
        index = users.index(team_member.user.username)
        try:
          scoreboard = Scoreboard.objects.get(event=team_member.event, team=team_member.team)
          points[index] = points[index] + scoreboard.score
          num_events[index] = num_events[index] + 1
        except:
          pass
      except:
        users.append(team_member.user.username)
        try:
          scoreboard = Scoreboard.objects.get(event=team_member.event, team=team_member.team)
          points.append(scoreboard.score)
          num_events.append(1)
        except:
          points.append(0)
          num_events.append(0)

    overall_standings = []
    for user in users:
      data_user = []
      data_user.append(user)
      index = users.index(user)
      data_user.append(points[index])
      data_user.append(num_events[index])
      found = 0
      for i in range(len(LEVEL)):
        if points[index] <= 0 and found == 0:
          data_user.append(LEVEL[0][0])
          found = 1
        if i == len(LEVEL)-1 and found == 0:
          if points[index] > LEVEL[i][1]:
            data_user.append(LEVEL[i][0])
          else:
            data_user.append(LEVEL[i-1][0])
          found = 1
        elif points[index] > LEVEL[i][1] and points[index] <= LEVEL[i+1][1] and found == 0:
          #if points[index] <= LEVEL[i][1] and found == 0:
          data_user.append(LEVEL[i][0])
          found = 1
      overall_standings.append(data_user)

    """Ordena la lista overall_standings por el metodo burbuja mejorado y 
       ademas sale del ciclo de pasadas, en cuanto detecta 
       que al final de una pasada no se realizaron 
       intercambios.""" 
    interchanges=1
    iteration=1
    while iteration<len(overall_standings) and interchanges==1:
      interchanges=0
      for i in range(0,len(overall_standings)-iteration):
        if overall_standings[i][1] < overall_standings[i+1][1]:
          overall_standings[i], overall_standings[i+1] = overall_standings[i+1], overall_standings[i]
          interchanges=1
      iteration += 1
    
    if many == "all" or many == None:
      return overall_standings
    else:
      many = int(many)
      return overall_standings[0:many]
