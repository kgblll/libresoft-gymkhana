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
#=

from apps.gymkhana.models import *
from apps.gymkhana.core.utils import *
import api

def create(event, challenge, picture, max_score, can_skip, challenge_type, is_stop, position, target_place, min_distance, mark_place, augmented_reality, learning_objectives):
    new_challenge = Challenge()
    new_challenge.event = event
    new_challenge.challenge = challenge
    if picture != None:
      new_challenge.picture = picture
    new_challenge.max_score = max_score
    new_challenge.augmented_reality = augmented_reality
    if new_challenge.max_score < 10:
      new_challenge.max_score = 10

    new_challenge.can_skip = can_skip
    new_challenge.challenge_type = challenge_type
    new_challenge.is_stop = is_stop

    if challenge_type == GEOLOCATION_CHALLENGE: # Prueba de geolocalizacion
      new_challenge.target_place = target_place
      new_challenge.distance_to_target_place = min_distance
      new_challenge.mark_place = mark_place

    # Inserto la nueva prueba en la posicion dada, y cambio el numero de prueba de todas las posteriores:
    challenges = event.challenge_set.all()
    try:
      if position != "None": # Insertar prueba en posicion dada:
        if challenges:
          challenge = challenges.get(id=position)
          numeral_position = challenge.number
          new_challenge.number = numeral_position
          for challenge in challenges:
            if (challenge.number >= numeral_position):
              challenge.number = challenge.number+1;
              challenge.save()
          if len(challenges) == int(1):
            challenge = challenges.get(id=position)
            new_challenge.next_challenge_id = challenge.id
            new_challenge.save()
            challenge.next_challenge_id = new_challenge.id
            challenge.save()
          else:
            challenge = challenges.get(id=position)
            previous_challenge = challenges.get(next_challenge_id=challenge.id)
            new_challenge.next_challenge_id = challenge.id
            new_challenge.save()
            previous_challenge.next_challenge_id = new_challenge.id
            previous_challenge.save()
            challenge.save()
      else: # Anyadir prueba al final del resto:
        if len(challenges) > int(1):
          new_challenge.number = len(challenges)+1
          last_challenge = challenges.get(number=len(challenges))
          first_challenge = challenges.get(number=int(1))
          new_challenge.next_challenge_id = first_challenge.id
          new_challenge.save()
          last_challenge.next_challenge_id = new_challenge.id
          last_challenge.save()
        elif len(challenges) == int(1):
          new_challenge.number = len(challenges)+1
          last_challenge = event.challenge_set.get(number=int(1))
          new_challenge.next_challenge_id = last_challenge.id
          new_challenge.save()
          last_challenge.next_challenge_id = new_challenge.id
          last_challenge.save()
        else:
          new_challenge.number = 1
          new_challenge.next_challenge_id = -1
    except: # Salta cuando no hay ninguna prueba y vamos a crear la primera
      new_challenge.number = 1
      new_challenge.next_challenge_id = -1

    new_challenge.save()

    for learning_objective in learning_objectives:
      new_challenge.objectives.add(learning_objective)
    new_challenge.save()

    event.score = event.score + new_challenge.max_score
    event.save()

    return True, new_challenge

def delete(event, challenge_id):
    challenges = event.challenge_set.all().order_by('number')
    for challenge in challenges:
      if challenge.id == challenge_id:
        challenge_to_delete = challenge

    challenge_number = challenge_to_delete.number

    # Reenlazo la lista sacando de ella la prueba que borramos:
    if len(event.challenge_set.all()) > int(2):
      previous_challenge = event.challenge_set.get(next_challenge_id=challenge_to_delete.id)
      next_challenge = event.challenge_set.get(id=challenge_to_delete.next_challenge_id)
      previous_challenge.next_challenge_id = next_challenge.id
      previous_challenge.save()
    elif len(event.challenge_set.all()) == int(2):
      challenge = event.challenge_set.get(id=challenge_to_delete.next_challenge_id)
      challenge.next_challenge_id = -1
      challenge.save()

    possible_solutions = challenge_to_delete.solution_set.all()
    for possible_solution in possible_solutions:
      possible_solution.delete()
    responses = challenge.response_set.all()
    for response in responses:
      correct, manager = api.manager.show(event)
      response.delete(manager.user)
    clues = challenge.clue_set.all()
    for clue in clues:
      clue.delete()
    try: # Necesito hacer esto porque sino, al eliminar la prueba, recursivamente por las relaciones, borra los equipos
      all_teams = Team.objects.all()
      teams = challenge_to_delete.team_set.all()
      for team in teams:
        first_challenge = FirstChallenge(event=event,team=team,first_challenge=None)
        first_challenge.save()
        team.save()
    except:
      pass
    challenge_to_delete.delete()

    challenges = event.challenge_set.all().order_by('number')
    for challenge in challenges:
      if (challenge.number > int(challenge_number)):
        challenge.number = challenge.number-1;
        challenge.save()

    event.score = event.score - challenge_to_delete.max_score
    event.save()

    return True, "No Error."

def delete_skip_challenge(team, challenge):
    try:
      skipped = SkippedChallenge.objects.get(challenge=challenge, team=team)
      skipped.delete()
    except:
      skipped = SkippedChallenge(challenge=challenge,team=team)
      skipped.delete()
    return True

def skip(team, challenge):
    try:
      skipped_challenge = SkippedChallenge.objects.get(challenge=challenge,team=team)
    except:
      skipped_challenge = SkippedChallenge(challenge=challenge,team=team)
      skipped_challenge.save()
    return True, skipped_challenge

def skipped_list(team):
    skipped_challenges = SkippedChallenge.objects.filter(team=team).order_by("id")
    return True, skipped_challenges

def respond(event, team, challenge, response_to_challenge, CORRECTION_FACTOR, position, altitude, distance_difference):
    scoreboard = Scoreboard.objects.get(event=event,team=team)
    if challenge.challenge_type == PHOTO_CHALLENGE: # Si es una prueba fotografica
      correct, result = api.response.create(team, challenge, None, response_to_challenge, True, position, altitude, distance_difference)
      message = "Continue"
      #response = "PENDING"
      #is_correct = False
      #scoreboard.num_incorrect_responses = scoreboard.num_incorrect_responses + 1
      response = "CORRECT"
      is_correct = True
      scoreboard.num_correct_responses = scoreboard.num_correct_responses + 1
    elif challenge.challenge_type == GEOLOCATION_CHALLENGE:
      correct, result = api.response.create(team, challenge, None, None, True, position, altitude, distance_difference)
      message = "Continue"
      response = "CORRECT"
      is_correct = True
      scoreboard.num_correct_responses = scoreboard.num_correct_responses + 1
    else:
      solutions = challenge.solution_set.all()
      success = 0
      for solution in solutions:
        if response_to_challenge.lower().strip() == solution.possible_solution.lower().strip():
          success = 1

      #scoreboard = Scoreboard.objects.get(event=event,team=team)
      if success == 1:
        response = "CORRECT"
        scoreboard.num_correct_responses = scoreboard.num_correct_responses + 1
        message = "Continue"
      else:
        response = "INCORRECT"
        scoreboard.num_incorrect_responses = scoreboard.num_incorrect_responses + 1
        if challenge.is_stop == True:
          message = "Repeat"
        else:
          message = "Continue"
      scoreboard.save()

      if response == "CORRECT":
        is_correct = True
      else:
        is_correct = False

      correct, result = api.response.create(team, challenge, response_to_challenge, None, is_correct, position, altitude, distance_difference)

    #scoreboard = Scoreboard.objects.get(event=event,team=team)
    if is_correct:
      scoreboard.score = scoreboard.score + challenge.max_score
    else:
      scoreboard.score = scoreboard.score - round(challenge.max_score * CORRECTION_FACTOR)
    scoreboard.save()

    return True, response, message
