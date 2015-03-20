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
from apps.gymkhana.core.utils import *

from django.contrib.gis.geos import Point

def create(event, text, from_team_id, from_manager_id, to, to_team_id, to_manager_id, to_team, manager, position, altitude):
    new_message = Message(event=event, text=text)
    if position != None:
      new_message.position = position
    else:
      new_message.position = Point(0.0, 0.0, srid=4326)
    if altitude != None:
      new_message.altitude = altitude
    else:
      new_message.altitude = 0.0

    if from_team_id != -1:
      correct, result = get_team(event, from_team_id)
      if correct:
        team = result
        new_message.from_team = team
      else:
        return False, render_to_response('error.' + format, {'code': 400, 'description': result})
    elif from_manager_id != -1:
      correct, result = get_manager_by_id(event,from_manager_id)
      if correct:
        from_manager = result
        new_message.from_manager = from_manager
      else:
        return False, render_to_response('error.' + format, {'code': 400, 'description': result})

    if to == "all": # Considero que solo admin puede enviar a all (teams mas manager)
      #if from_manager != None:
      teams = event.team_set.all()
      for team in teams:
        if from_team_id != team.id:
          new_message.to_manager = manager
          new_message.save()
          new_message.to_team.add(team)
      #new_message.to_manager = from_manager
      new_message.save()
    elif to == "manager":
      correct, result = get_manager(event)
      if correct:
        new_message.to_manager = result
        new_message.save()
      else:
        return False, render_to_response('error.' + format, {'code': 400, 'description': result})
    elif to_team != None:
      #message = Message(event=event, text=text, from_team=new_message.from_team, from_manager=new_message.from_manager)
      #message = Message(event=event, text=text, from_team=new_message.from_team)
      new_message.save()
      new_message.to_team.add(to_team)

    return True, "ok"

def list(event):
    messages = event.message_set.all().order_by("date")
    return True, messages

def delete(message):
    correct, manager = get_manager(message.event)
    message.delete(manager.user)
    return True, "ok"

def delete_all(event):
    event.message_set.all().delete()
    return True, "ok"

def reply(message):
    text_to_reply = "\n\n\n\n"

    to_manager = None
    from_manager = None
    team_to_reply = None

    if message.from_manager != None:
      to_manager = message.from_manager
      from_manager = message.from_manager
      text_to_reply = text_to_reply + "Manager " + message.from_manager.user.username
    if message.from_team != None:
      team_to_reply = message.from_team
      text_to_reply = text_to_reply + "Team " + message.from_team.group.name
    if message.to_manager != None:
      from_manager = message.to_manager
    if message.to_team.all() != None:
      to_teams = message.to_team.all()
      if len(to_teams) == 1:
        for to_team in to_teams:
          team_to_reply = to_team

    text_to_reply = text_to_reply + " wrote (" + str(message.date) + "):\n\n>>" + message.text

    return True, "ok", to_manager, team_to_reply, from_manager, to_teams, text_to_reply

def list_by_team(event, team, type):
    if type.strip().lower() == "sent":
      messages = event.message_set.filter(from_team=team).order_by("date")
    elif type.strip().lower() == "inbox":
      messages = event.message_set.filter(to_team=team).order_by("date")
    else:
      return False, "Invalid Option \"" + type + "\"." 
    return True, messages
