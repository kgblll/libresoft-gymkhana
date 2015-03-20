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

from social.core import api as api_lgs
from apps.gymkhana.models import *
from apps.gymkhana.core.utils import *
import api

from django.contrib.gis.geos import Point

def subscribe_to_event(event, team, first_challenge_team_id):

    team.event.add(event)

    if first_challenge_team_id != "None":
      correct, result = get_challenge(event, int(first_challenge_team_id.strip()))
      if correct:
        challenge = result
        try:
          first_challenge = FirstChallenge.objects.get(event=event,team=team)
          first_challenge.delete()
        except:
          pass
        first_challenge = FirstChallenge(event=event,team=team,first_challenge=challenge)
        first_challenge.save()
      else:
        return False, result
    elif first_challenge_team_id == "None":
      try:
        first_challenge = FirstChallenge.objects.get(event=event,team=team)
        first_challenge.delete()
      except:
        pass

    create_scoreboard(event, team)
    team.save()
    return True, "ok"

def join_to_event(event, team):
    create_scoreboard(event,team)

    responses = team.responses.all()
    try:
      correct, manager = api.manager.show(event)
      for response in responses:
        if response.challenge.event == event:
          response.delete(manager.user)
    except:
      pass

    skipped_challenges = SkippedChallenge.objects.filter(team=team)
    for skipped_challenge in skipped_challenges:
      if skipped_challenge.challenge.event == event:
        skipped_challenge.delete()

    acquired_clues = AcquiredClue.objects.filter(team=team)
    for acquired_clue in acquired_clues:
      acquired_clue.delete()

    team.save()
    first_challenge = FirstChallenge.objects.get(event=event,team=team)
    return True, "ok", first_challenge

def unjoin(event, team):
    team.event.delete(event)
    return True, "ok"

def list(event):
    teams = event.team_set.all()
    # Esto lo hago para comprobar que hay al menos un equipo con una primera prueba configurada. Si no hay
    # ningun equipo con primera prueba configurada, es como si no existiera puesto que no podra competir:
    success = 0
    first_challenges = FirstChallenge.objects.filter(event=event)
    for team in teams:
      for first_challenge in first_challenges:
        if first_challenge.team == team:
          success = 1

    finished_s = Finished.objects.filter(event=event)

    # Realmente, luego en la plantilla solo volcare la info de los equipos que tienen definida una primera prueba.

    scoreboards = Scoreboard.objects.filter(event=event).order_by('-score') # - para ordenar en orden descendente en list_team.json

    return True, "ok", teams, first_challenges, scoreboards, finished_s, success

#def list(event, order):
#    teams = event.team_set.all()
#    # Esto lo hago para comprobar que hay al menos un equipo con una primera prueba configurada. Si no hay
#    # ningun equipo con primera prueba configurada, es como si no existiera puesto que no podra competir:
#    success = 0
#    first_proofs = FirstProof.objects.filter(event=event)
#    for team in teams:
#      for first_proof in first_proofs:
#        if first_proof.team == team:
#          success = 1
#
#    # Realmente, luego en la plantilla solo volcare la info de los equipos que tienen definida una primera prueba.
#
#    scoreboards = Scoreboard.objects.filter(event=event).order_by('-score') # - para ordenar en orden descendente en list_team.json
#
#    return True, "ok", teams, first_proofs, scoreboards, success

def list_all():
    return True, Team.objects.all()

def list_order_by_id(event):
  return True, event.team_set.all().order_by("id")

def create(event, teamname, num_first_challenge_id):
    group = {'groupname': teamname.strip()}
    correct, message = api_lgs.group.create_or_modify(group, modify=False)
    if correct:
      # message almacena group.id cuando todo ha ido correctamente
      group = Group.objects.get(id=message)
      if num_first_challenge_id != -1:
        first_challenge = event.challenge_set.get(id=num_first_challenge_id)
        team = Team(group=group)
        team.save()
        create_scoreboard(event,team)
        team.event.add(event)
        first_challenge = FirstChallenge(event=event,team=team,first_challenge=first_challenge)
        first_challenge.save()
      else:
        team = Team()
        team.group = group
        team.save()
        create_scoreboard(event,team)
        team.event.add(event)
        team.save()
      return True, team
    else:
      return False, "The Group \'" + teamname + "\' Already Exists In LibreGeoSocial."

def edit_first_challenge(event, team, challenge):
    try:
      first_challenge = FirstChallenge.objects.get(event=event,team=team)
      first_challenge.delete()
    except:
      pass
    first_challenge = FirstChallenge(event=event,team=team,first_challenge=challenge)
    first_challenge.save()
    team.save()
    return True, "ok"

def edit_position(team, longitude, latitude):
    point = Point(longitude, latitude, srid=4326)
    team.group.position = point
    team.group.save()
    team.save()
    return True, "ok"

def show(event, team):
    team_members = TeamMember.objects.filter(event=event, team=team)
    #team_members = team.teammember_set.get()
    scoreboard = Scoreboard.objects.get(event=event,team=team)
    try:
      first_challenge = FirstChallenge.objects.get(event=event,team=team)
    except:
      first_challenge = None
    return True, "ok", team_members, first_challenge, scoreboard

def delete(team, manager):
    team_members = team.teammember_set.all()
    if len(team_members) > 0:
      for team_member in team_members:
        team_member.delete()
    team.group.delete(manager.user.id) # Lo elimino puesto que no dejo enlazar grupos ya creados; cada nuevo team, un nuevo group.
    team.responses.all().delete()
    acquired_clues = AcquiredClue.objects.filter(team=team)
    for acquired_clue in acquired_clues:
      acquired_clue.delete()
    scoreboards = Scoreboard.objects.all()
    for scoreboard in scoreboards:
      if scoreboard.team == team:
        scoreboard.delete()
    team.delete()
    return True, "ok"

def save_parameters(event_id, team_id, date, length):
    parameters = Parameters(event_id=event_id, team_id=team_id, time=date, length=length)
    parameters.save()
    return True, parameters

def delete_parameters(event_id, team_id):
    try:
      parameters = Parameters.objects.filter(event_id=event_id, team_id=team_id)
      parameters.delete()
      return True, "ok"
    except:
      return False, "error"

def getParameters(event_id, team_id):
    list_parameters = Parameters.objects.filter(event_id=event_id, team_id=team_id)
    if list_parameters:
      correct = True
    else:
      correct = False
    return correct, list_parameters

