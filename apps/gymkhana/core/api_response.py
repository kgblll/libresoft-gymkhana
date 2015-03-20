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
from social.core.models import Social_node
from apps.gymkhana.core.utils import *

def edit(response, event, team, CORRECTION_FACTOR):
    if response.is_correct == False:
      response.is_correct = True
      scoreboard = Scoreboard.objects.get(event=event,team=team)
      scoreboard.num_correct_responses = scoreboard.num_correct_responses + 1
      scoreboard.num_incorrect_responses = scoreboard.num_incorrect_responses - 1
      scoreboard.score = scoreboard.score + response.challenge.max_score + round(response.challenge.max_score * CORRECTION_FACTOR)
      scoreboard.save()
    else:
      response.is_correct = False
      scoreboard = Scoreboard.objects.get(event=event,team=team)
      scoreboard.num_correct_responses = scoreboard.num_correct_responses - 1
      scoreboard.num_incorrect_responses = scoreboard.num_incorrect_responses + 1
      scoreboard.score = scoreboard.score - response.challenge.max_score - round(response.challenge.max_score * CORRECTION_FACTOR)
      scoreboard.save()
    team.save()
    return True, "ok"

def delete(response, event, team, CORRECTION_FACTOR):
    scoreboard = Scoreboard.objects.get(event=event,team=team)
    if response.is_correct:
      scoreboard.score = scoreboard.score - response.challenge.max_score
      scoreboard.num_correct_responses = scoreboard.num_correct_responses - 1
    else:
      scoreboard.score = scoreboard.score + round(response.challenge.max_score * CORRECTION_FACTOR)
      scoreboard.num_incorrect_responses = scoreboard.num_incorrect_responses - 1
    scoreboard.save()
    team.save()
    try:
      team_member = TeamMember.objects.get(event=event, team=team)
      response.delete(team_member.user)
    except:
      correct, manager = get_manager(event)
      response.delete(manager.user)

    return True, "ok"

def create(team, challenge, response_to_challenge, photo, is_correct, position, altitude, distance_difference):
    new_response = Response(challenge=challenge, position=position, altitude=altitude)
    if photo != None:
      #new_response.response = null
      new_response.is_correct = is_correct
      new_response.photo = photo
    elif challenge.challenge_type == GEOLOCATION_CHALLENGE:
      new_response.is_correct = is_correct
      new_response.distance_difference = distance_difference
    else:
      new_response.response_text = response_to_challenge
      new_response.is_correct = is_correct
    new_response.save()
    new_response.response_text
    team.responses.add(new_response)
    team.save()
    return True, new_response
