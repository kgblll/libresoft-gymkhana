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

def create(title, place, celebration, language, image, configurate_teams, welcome_text, goodbye_text, manager_id, difficulty, learning_objectives):
    new_event = Event()
    #date= datetime.date.today()
    #today= fecha.strftime("%d/%m/%Y")
    new_event.title = title
    new_event.place = place
    new_event.celebration = celebration
    new_event.language = language
    new_event.image = image
    new_event.configurate_teams = configurate_teams
    new_event.welcome_text = welcome_text
    new_event.goodbye_text = goodbye_text
    new_event.difficulty = difficulty
    new_event.save()

    for learning_objective in learning_objectives:
      new_event.objectives.add(learning_objective)
    new_event.save()

    user = Person.objects.get(id=manager_id)
    manager = Manager.objects.get(user=user)
    manager.events.add(new_event)
    manager.save()

    return True, new_event

def show(event):
    challenges = event.challenge_set.all().order_by('number')
    teams = event.team_set.all()
    first_challenges = FirstChallenge.objects.filter(event=event)
    try:
      manager = Manager.objects.get(events__id=event.id)
    except:
      manager = None

    return True, challenges, teams, first_challenges, manager

def set_status(event):
    if event.is_closed:
      event.is_closed = False
    else:
      event.is_closed = True
    event.save()
    return True, event

def delete(event):
    challenges = event.challenge_set.all().order_by('number')
    if len(challenges) > 0:
      for challenge in challenges:
        possible_solutions = challenge.solution_set.all()
        for possible_solution in possible_solutions:
          possible_solution.delete()
        responses = challenge.response_set.all()
        for response in responses:
          team_member = TeamMember.objects.get(event=event, team=team)
          response.delete(team_member.user)
        challenge.delete()

    teams = event.team_set.all()
    if len(teams) > 0:
      for team in teams:
        team_members = team.teammember_set.all()
        if len(team_members) > 0:
          for team_member in team_members:
            team_member.delete()
        responses = team.responses.all()
        for response in responses:
          if response.challenge.event == event:
            team_member = TeamMember.objects.get(event=event, team=team)
            response.delete(team_member.user)
        #team.group.delete() # Lo elimino puesto que no dejo enlazar grupos ya creados; cada nuevo team, un nuevo group.
        #team.responses.all().delete()
        acquired_clues = AcquiredClue.objects.filter(team=team)
        for acquired_clue in acquired_clues:
          if acquired_clue.clue.challenge.event == event:
            acquired_clue.delete()
        #team.delete()

    event.delete()
    return True, "No Error."

def list_all():
    return True, Event.objects.all()
