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

from django.contrib.gis.geos import Point

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
import random
from django.views.decorators.csrf import csrf_exempt

from social.core import api as api_lgs
from social.rest.forms import LoginForm

from apps.gymkhana.models import *
from apps.gymkhana.core.utils import *

from apps.gymkhana.core import api

DEFAULT_MANAGER_USERNAME = 'manager'
DEFAULT_MANAGER_PASSWORD = 'manager'

DEFAULT_FORMAT = 'html'

CORRECTION_FACTOR = 0.1

@csrf_exempt
def user_create(request):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    is_admin = False
    correct, managers = api.manager.list_all()
    if correct:
      for manager in managers:
        if request.user.username == manager.user.username:
          is_admin = True

    if request.method == "GET":
      return render_to_response('create_user.' + format, {'code': 200, 'description': 'ok', 'logged_user_is_admin': is_admin })
    elif request.method == "POST":
      if ("password" in request.POST) and ("username" in request.POST) and ("first_name" in request.POST) and ("last_name" in request.POST):
        user = {'username': request.POST["username"].strip(), 'password': request.POST["password"],
                'first_name': request.POST["first_name"].strip(), 'last_name': request.POST["last_name"].strip()}
        correct, message = api_lgs.user.create_or_modify(user, modify=False)

        if is_admin:
          if "is_manager" in request.POST and request.POST['is_manager'] == 'True':
            new_user = Person.objects.get(id=message)
            new_manager = Manager(user=new_user)
            new_manager.save()

        if correct:
          url = "/gymkhana/user/login"
          return HttpResponseRedirect(url)
        else:
          return render_to_response('error.' + format, {'code': 500, 'description': message})
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "Missing Parameters."})
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

@csrf_exempt
def user_logout(request):
    logout(request)
    # Redirect to a success page.
    url = "/gymkhana/user/login/"
    return HttpResponseRedirect(url)

@csrf_exempt
def user_login(request):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if request.method == "GET":
      correct, managers = api.manager.list_all()
      if len(managers) == 0:
        manager = {'username': DEFAULT_MANAGER_USERNAME, 'password': DEFAULT_MANAGER_PASSWORD}
        correct, message = api_lgs.user.create_or_modify(manager, modify=False)
        if correct:
          user = Person.objects.get(id=message)
          default_manager = Manager(user=user)
          default_manager.save()
          return render_to_response('login.' + format, {'code': 200, 'description': 'ok'})
        else:
          return render_to_response('error.' + format, {'description': message})
      return render_to_response('login.' + format, {'code': 200, 'description': 'ok'})
    elif request.method == "POST":
      loginform = LoginForm(request.POST)
      id = loginform.login(request)
      if id:
        # Redirect to a success page.
        url = "/gymkhana/event/list/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "Username and Password Do Not Match."})
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

@csrf_exempt
def user_list(request):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if format != "html":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Format."})

    if not request.user.is_authenticated():
      url = "/gymkhana/user/login/"
      return HttpResponseRedirect(url)

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    logged_user_is_admin = check_session_user_type(request)
    if logged_user_is_admin:
      users = Person.objects.all().order_by('id')
      return render_to_response('list_user.' + format, {'code': 200, 'description': 'ok', 'users': users})
    else:
      return render_to_response('error.' + format, {'code': 401, 'description': 'You are not authorized to execute this action.'})

@csrf_exempt
def user_edit(request, user_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    logged_user_is_admin = check_session_user_type(request)
    if logged_user_is_admin:
      correct, user = get_user(user_id)
      if not correct:
        return render_to_response('error.' + format, {'code': 400, 'description': "The user does not exist."})
      is_admin = check_user_type(user)
      if not is_admin:
        new_manager = Manager(user = user)
        new_manager.save()
      else:
        managers = Manager.objects.all()
        for manager in managers:
          if manager.user == user:
            manager.delete()
      is_admin = check_user_type(user)
      logged_user_is_admin = check_session_user_type(request)
      url = "/gymkhana/user/" + str(user.id) + "/show"
      return HttpResponseRedirect(url)
      #return render_to_response('show_user.' + format, {'code': 200, 'description': "ok", 'user': user, 'isAdmin': is_admin, 'logged_user_is_admin': logged_user_is_admin})
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': "You must be a manager to execute this action."})

@csrf_exempt
def user_delete(request, user_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    logged_user_is_admin = check_session_user_type(request)
    if logged_user_is_admin:
      correct, user = get_user(user_id)
      if not correct:
        return render_to_response('error.' + format, {'code': 400, 'description': "The user does not exist."})
      is_admin = check_user_type(user)
      managers = Manager.objects.all()
      for manager in managers:
        if manager.user == user:
          manager.delete()
      user.delete()
      url = "/gymkhana/user/list/"
      return HttpResponseRedirect(url)
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': "You must be a manager to execute this action."})

@csrf_exempt
def user_show(request, user_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    correct, result = get_user(user_id)
    if correct:
      user = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': 'The User is not Authenticated.'})

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    isAdmin = check_user_type(user)
    loggedUserIsAdmin = check_session_user_type(request)
    return render_to_response('show_user.' + format, {'code': 200, 'description': 'ok', 'user': user, 'isAdmin': isAdmin, 'logged_user_is_admin': loggedUserIsAdmin})

@csrf_exempt
def event_list(request):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    #if check_logged_user(request) == False:
    #  if format == 'html':
    #    url = "/gymkhana/user/login/"
    #    return HttpResponseRedirect(url)
    #  else:
    #    return render_to_response('error.' + format, {'code': 400, 'description': 'The User is not Authenticated.'})

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    correct, events = api.event.list_all()
    isAdmin = check_session_user_type(request)
    correct, managers = api.manager.list_all()
    if len(events) == 0:
      return render_to_response('list_event.' + format, {'code': 200, 'description': 'There Are No Events', 'isAdmin': isAdmin, 'managers': managers})
    else:
      return render_to_response('list_event.' + format, {'code': 200, 'description': 'ok', 'events': events, 'isAdmin': isAdmin, 'managers': managers})

@csrf_exempt
def event_create(request):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    if check_session_user_type(request) == False: # Si no es administrador, no le dejamos crear eventos:
      return render_to_response('error.' + format, {'code': 200, 'description': "Only a Manager Can Create a New Event."})

    if request.method == "GET":
      return render_to_response('create_gymkhana.' + format, {'code': 200, 'description': 'ok'})
    elif request.method == "POST":
      # Cargo la foto si es que el manager la ha enviado.
      correct, result = read_photo(request)
      if correct:
        image = result
      else:
        image = None
        return render_to_response('error.' + format, {'code': 400, 'description': result})

      if request.POST["title"].strip() != "" and request.POST["place"].strip() != "" and request.POST["celebration"].strip() != "" and request.POST["welcome_text"].strip() != "" and request.POST["goodbye_text"].strip() != "":
        title = request.POST["title"].strip()
        place = request.POST["place"].strip()
        celebration = request.POST["celebration"].strip()
        language = request.POST["language"].strip()
        configurate_teams = request.POST["configurate_teams"].strip()
        if configurate_teams == "yes":
          configurate_teams = True
        else:
          configurate_teams = False
        if "difficulty" in request.POST:
          difficulty = int(request.POST["difficulty"].strip())
        else:
          difficulty = 3
        welcome_text = request.POST["welcome_text"].strip()
        goodbye_text = request.POST["goodbye_text"].strip()
        manager_id = request.session["_auth_user_id"]

        learning_objectives = []
        num_learning_objectives = int(request.POST["select_num_learning_objectives"].strip())
        for i in range(num_learning_objectives):
          if (request.POST["learning_objective_" + str(i+1)].strip() == ""):
            return render_to_response('error.' + format, {'code': 300, 'description': "A learning objective is blank."})
          else:
            correct, learning_objective = api.learning_objective.create(request.POST["learning_objective_" + str(i+1)].strip())
            if correct:
              learning_objectives.append(learning_objective)

        correct, result = api.event.create(title, place, celebration, language, image, configurate_teams, welcome_text, goodbye_text, manager_id, difficulty, learning_objectives)
        if correct:
          new_event = result
          url = "/gymkhana/event/" + str(new_event.id) + "/show/"
          return HttpResponseRedirect(url)
        else:
          return render_to_response('error.' + format, {'code': 400, 'description': "Internal Error. " + result})
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

@csrf_exempt
def event_show(request, event_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': 'The User is not Authenticated.'})

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    correct, challenges, teams, first_challenges, manager = api.event.show(event)
    correct, solutions = api.solution.list_all()
    correct, all_teams = api.team.list_all()
    isAdmin = check_session_user_type(request)
    try:
      #manager = Manager.objects.get(events__id=event.id)
      return render_to_response('show_gymkhana.' + format, {'code': 200, 'description': 'ok', 'event': event, 'challenges': challenges, 'num_challenges': len(challenges), 'teams': teams, 'num_teams': len(teams), 'all_teams': all_teams, 'first_challenges': first_challenges, 'manager': manager, 'isAdmin': isAdmin})
    except:
      return render_to_response('show_gymkhana.' + format, {'code': 200, 'description': 'ok', 'event': event, 'challenges': challenges, 'num_challenges': len(challenges), 'teams': teams, 'num_teams': len(teams), 'all_teams': all_teams, 'first_challenges': first_challenges, 'isAdmin': isAdmin})

@csrf_exempt
def event_delete(request, event_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': 'The User is not Authenticated.'})

    if check_session_user_type(request) == False: # Si no es administrador, no puede eliminar:
      return render_to_response('error.' + format, {'code': 200, 'description': "You Can't Delete an Event."})

    correct, message = api.event.delete(event)
    if correct:
      return HttpResponseRedirect('/gymkhana/event/list/')
    else:
      return render_to_response('error.' + format, {'code': 500, 'description': "Internal Error. " + message})

@csrf_exempt
def event_set_status(request, event_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': 'The User is not Authenticated.'})

    if check_session_user_type(request) == False: # Si no es administrador, no puede eliminar:
      return render_to_response('error.' + format, {'code': 200, 'description': "You Can't Delete an Event."})

    correct, event = api.event.set_status(event)
    if correct:
      return HttpResponseRedirect('/gymkhana/event/' + event_id + '/show/')
    else:
      return render_to_response('error.' + format, {'code': 500, 'description': "Internal Error. " + message})

@csrf_exempt
def challenge_create(request, event_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': 'The User is not Authenticated.'})

    if check_session_user_type(request) == False: # Si no es administrador, no puede crear pruebas:
      return render_to_response('error.' + format, {'code': 200, 'description': "You Can't Create a New Challenge."})

    if request.method != "POST":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    if "challenge" in request.POST and "max_score" in request.POST and "challenge_type" in request.POST:
      pass
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': "Missing Parameters."})

    # Compruebo que no esten vacios el reto y la maxima puntuacion de la prueba
    if (request.POST["challenge"].strip() == ""):
      return render_to_response('error.' + format, {'code': 400, 'description': "Challenge is Empty."})
    else:
      challenge = request.POST["challenge"].strip()

    if (request.POST["max_score"].strip() == ""):
      return render_to_response('error.' + format, {'code': 400, 'description': "Maximum Score is Empty."})
    else:
      max_score = int(request.POST["max_score"].strip())

    if request.POST["can_skip"].strip().lower() == "yes":
      can_skip = True
    else:
      can_skip = False

    if request.POST["is_stop"].strip().lower() == "yes":
      is_stop = True
    else:
      is_stop = False

    challenge_type = -1
    augmented_reality = False
    if int(request.POST["challenge_type"].strip()) == TEXTUAL_CHALLENGE:
      challenge_type = 1
      try:
        if request.POST["augmented_reality"].strip().lower() == "yes":
          augmented_reality = True
        else:
          augmented_reality = False
      except:
        augmented_reality = False
    elif int(request.POST["challenge_type"].strip()) == PHOTO_CHALLENGE:
      challenge_type = 2
      is_stop = False
    elif int(request.POST["challenge_type"].strip()) == GEOLOCATION_CHALLENGE:
      challenge_type = 3
      is_stop = False

    if challenge_type == TEXTUAL_CHALLENGE: # Si es prueba textual
      if "select_num_possible_solutions" in request.POST and "possible_solution_1" in request.POST and "select_num_clues" in request.POST:
        pass
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "Missing Parameters."})

    target_place = None
    mark_place = None
    min_distance = -1
    if challenge_type == GEOLOCATION_CHALLENGE: # Si es prueba de localizacion
      if "target_latitude" in request.POST and "target_longitude" in request.POST and "min_distance" in request.POST and "mark_target_place" in request.POST:
        try:
          target_latitude = float(request.POST["target_latitude"])
          target_longitude = float(request.POST["target_longitude"])
          target_place = Point(target_longitude, target_latitude, srid=4326)
          min_distance = float(request.POST["min_distance"])
          mark_place = str(request.POST["mark_target_place"]).strip().lower()
          if mark_place == "yes":
            mark_place = True
          else:
            mark_place = False
        except:
          return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Value for \'target_latitude\' / \'target_longitude\' / \'min_distance\' / \'mark_target_place\' Parameter/s."})
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "Missing \'target_latitude\' / \'target_longitude\' Parameter/s."})

    # Compruebo que no esten vacias ni las posibles soluciones ni las pistas en caso de haberlas:
    if challenge_type == TEXTUAL_CHALLENGE: # Si es prueba textual
      num_possible_solutions = int(request.POST["select_num_possible_solutions"].strip())
      #if num_possible_solutions == 1:
      #  if (request.POST["possible_solution_1"].strip() == ""):
      #    return render_to_response('error.' + format, {'code': 400, 'description': "Solution is Empty."})
      #else:
      for i in range(num_possible_solutions):
        if (request.POST["possible_solution_" + str(i+1)].strip() == ""):
          return render_to_response('error.' + format, {'code': 400, 'description': "A Possible Solution is Empty."})
    num_clues = int(request.POST["select_num_clues"].strip())
    if num_clues >= 1:
      for i in range(num_clues):
        if (request.POST["clue_" + str(i+1)].strip() == ""):
          return render_to_response('error.' + format, {'code': 400, 'description': "Clue number " + str(i+1) +" is Empty."})

    if "position" in request.POST and request.POST["position"] != "None": # Insertar prueba en posicion dada:
      position = int(request.POST["position"].strip())
    else:
      position = "None"

    # Cargo la foto si es que el manager la ha enviado.
    correct, result = read_photo(request)
    if correct:
      picture = result
    else:
      picture = None

    learning_objectives = []
    for i in range(len(event.objectives.all())):
      try:
        learning_objective = LearningObjective.objects.get(id=int(request.POST["learning_objective_" + str(i+1)].strip()))
        learning_objectives.append(learning_objective)
      except:
        pass

    correct, result = api.challenge.create(event, challenge, picture, max_score, can_skip, challenge_type, is_stop, position, target_place, min_distance, mark_place, augmented_reality, learning_objectives)
    if correct:
      new_challenge = result
    else:
      return render_to_response('error.' + format, {'code': 500, 'description': "Internal Error. " + result})

    if new_challenge.challenge_type == TEXTUAL_CHALLENGE: # Es prueba textual
      num_possible_solutions = int(request.POST["select_num_possible_solutions"].strip())
      #if num_possible_solutions == 1:
      #  correct, result = api.solution.create(request.POST["possible_solution"].strip(), new_proof)
      #else:
      for i in range(num_possible_solutions):
        correct, result = api.solution.create(request.POST["possible_solution_" + str(i+1)].strip(), new_challenge)

    num_clues = int(request.POST["select_num_clues"].strip())
    if num_clues >= 1:
      for i in range(num_clues):
        correct, result = api.clue.create((i+1), request.POST["clue_" + str(i+1)].strip(), new_challenge, CORRECTION_FACTOR)

    url = "/gymkhana/event/" + str(event_id) + "/show/"
    return HttpResponseRedirect(url)

@csrf_exempt
def challenge_delete(request, event_id, challenge_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': 'The User is not Authenticated.'})

    if check_session_user_type(request) == False: # Si no es administrador, no puede eliminar:
      return render_to_response('error.' + format, {'code': 200, 'description': "You Can't Delete a Challenge."})

    correct, message = api.challenge.delete(event, int(challenge_id))
    if correct:
      url = "/gymkhana/event/" + str(event_id) + "/show/"
      return HttpResponseRedirect(url)
    else:
      return render_to_response('error.' + format, {'code': 500, 'description': "Internal Error. " + message})

@csrf_exempt
def challenge_show(request, event_id, challenge_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = get_challenge(event, challenge_id)
    if correct:
      challenge = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    #print request.META.get('REMOTE_ADDR', '<none>')

    #has_clues = "false"
    num_clues = len(Clue.objects.filter(challenge=challenge))
    #if num_clues > 0:
    #  has_clues = "true"

    description = "Challenge Correctly Sent."
    if challenge.challenge_type == GEOLOCATION_CHALLENGE:
      return render_to_response('challenge.' + format, {'code': 200, 'description': description, 'challenge': challenge.challenge, 'max_score': challenge.max_score, 'challenge_type': challenge.challenge_type, 'augmented_reality': challenge.augmented_reality, 'can_skip': challenge.can_skip, 'number': challenge.number, 'target_place': challenge.target_place, 'distance_to_target_place': challenge.distance_to_target_place, 'mark_place': challenge.mark_place, 'num_clues': num_clues, 'picture': challenge.picture})

    return render_to_response('challenge.' + format, {'code': 200, 'description': description, 'challenge': challenge.challenge, 'max_score': challenge.max_score, 'challenge_type': challenge.challenge_type, 'augmented_reality': challenge.augmented_reality, 'can_skip': challenge.can_skip, 'number': challenge.number, 'num_clues': num_clues, 'picture': challenge.picture})

@csrf_exempt
def challenge_respond(request, event_id, challenge_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = get_challenge(event, challenge_id)
    if correct:
      challenge = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if request.method != 'POST':
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    correct, result = get_team(event, request.POST['team_id'].strip())
    if correct:
      team = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if "latitude" in request.POST and "longitude" in request.POST and "altitude" in request.POST:
      latitude = float(request.POST['latitude'].strip())
      longitude = float(request.POST['longitude'].strip())
      altitude = float(request.POST['altitude'].strip())
      position = Point(float(longitude), float(latitude), srid=4326)
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': "Missing \'latitude\'/\'longitude\'/\'altitude\' Parameter/s."})

    response_to_challenge = None
    distance_difference = -1
    if challenge.challenge_type == PHOTO_CHALLENGE:
      correct, result = read_photo(request)
      if correct:
        response_to_challenge = result
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': result})
    elif challenge.challenge_type == TEXTUAL_CHALLENGE and 'response' in request.POST:
      response_to_challenge = request.POST['response'].strip()
    elif challenge.challenge_type == GEOLOCATION_CHALLENGE:
      if "success" in request.POST and "distance_difference" in request.POST:
        success = request.POST['success'].strip().lower()
        distance_difference = float(request.POST['distance_difference'].strip())
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "Missing \'success\'/\'distance_difference\' Parameter/s."})
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': "Missing \'response\' or \'photo\' Parameter."})

    correct, response, message = api.challenge.respond(event, team, challenge, response_to_challenge, CORRECTION_FACTOR, position, altitude, distance_difference)

    is_last_challenge, next_challenge_id = search_following_challenge(event, challenge, team, message)
    description = "Response Proccessed Succesfully."
    return render_to_response('solution.' + format, {'code': 200, 'description': description, 'solution': response, 'message': message, 'next_challenge_id': next_challenge_id, 'is_last_challenge': is_last_challenge})

@csrf_exempt
def team_subscribe(request, event_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': 'The User is not Authenticated.'})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if request.method != "POST":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    if "team_to_subscribe_id" in request.POST:
      team_id = int(request.POST["team_to_subscribe_id"].strip())
      correct, result = get_team_by_id(team_id)
      if correct:
        team = result
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': result})

      if "first_challenge_team_id" in request.POST:
        first_challenge_team_id = request.POST["first_challenge_team_id"]

      correct, result = api.team.subscribe_to_event(event, team, first_challenge_team_id)
      if correct and format == 'html':
        url = "/gymkhana/event/" + str(event_id) + "/show/"
        return HttpResponseRedirect(url)
      elif correct:
        return render_to_response('correct.' + format, {'code': 200, 'description': "ok"})
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': result})
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': "Missing Parameters."})

@csrf_exempt
def monitoring(request, event_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': 'The User is not Authenticated.'})

    if check_session_user_type(request) == False: # Solo el administrador puede monitorizar el evento:
      return render_to_response('error.' + format, {'code': 200, 'description': "You Can't Monitorize this Event."})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    if format != "html":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Format."})

    return render_to_response('monitoring.' + format, {'code': 200, 'description': 'ok', 'event': event})

@csrf_exempt
def team_join(request, event_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.html', {'code': 400, 'description': result})

    if "teamname" in request.GET:
      correct, result = get_team_by_name(event, request.GET["teamname"].strip())
      if correct:
        team = result
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': result})

      try:
        objetos = Finished.objects.all()
        finished = Finished.objects.get(event=event, team=team)
        if finished.is_finished: # Si el team ha acabado la gymkhana y quiere volverla a hacer
          finished.delete()
          team_members = TeamMember.objects.filter(event=event, team=team)
          for team_member in team_members:
            team_member.delete()
          teams = event.team_set.all()
          for team_1 in teams:
            if team_1 == team:
              #team_1.unjoin()
              correct, message = api.team.unjoin(event, team)
              team.responses.delete()
          correct, message, first_challenge = api.team.join_to_event(event, team)
          finished = Finished(event=event, team=team, is_finished=False)
          finished.save()
        else:
          correct, message = api.team_member.create_by_user_id(event, team, request.user.id)
          correct, message, current_challenge = get_current_challenge(event, team)
          return render_to_response('join_team.' + format, {'code': 200, 'description': "ok", 'first_challenge_id': current_challenge.id, 'team_id': team.id})
      except:
        finished = Finished(event=event, team=team, is_finished=False)
        finished.save()
        correct, message, first_challenge = api.team.join_to_event(event, team)
      correct, message = api.team_member.create_by_user_id(event, team, request.user.id)
      return render_to_response('join_team.' + format, {'code': 200, 'description': "ok", 'first_challenge_id': first_challenge.first_challenge.id, 'team_id': team.id})
    else:
      return render_to_response('join_team.' + format, {'code': 400, 'description': "Missing \'teamname\' Parameter."})

@csrf_exempt
def team_list(request, event_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})      
    
    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': 'The User is not Authenticated.'})

    #try:
    #  if "order_by" in request.GET:
    #    order = request.GET['order_by'].strip()
    #  else:
    #    order = "None"
    #except:
    #  order = "None"

    #correct, message, teams, first_proofs, scoreboards, success = api.team.list(event, order)
    correct, message, teams, first_challenges, scoreboards, finished_s, success = api.team.list(event)
    if not correct:
      return render_to_response('error.' + format, {'code': 400, 'description': "Internal Error. " + message})

    if format == 'html':
      isAdmin = check_session_user_type(request) # Hacer este html!
      return render_to_response('list_team.html', {'code': 200, 'description': 'ok', 'event': event, 'teams': teams, 'first_challenges': first_challenges, 'scoreboards': scoreboards, 'isAdmin': isAdmin})

    if len(teams) == 0 or success == 0:
      return render_to_response('list_team.' + format, {'code': 200, 'description': 'There Are No Teams Ready To Play.'})
    else:
      return render_to_response('list_team.' + format, {'code': 200, 'description': 'ok', 'event': event, 'teams': teams, 'first_challenges': first_challenges, 'scoreboards': scoreboards, 'finished_s': finished_s})

@csrf_exempt
def team_create(request, event_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})      

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': 'The User is not Authenticated.'})

    #if check_session_user_type(request) == False: # Si no es administrador, no puede crear equipos:
    #  error_message = "You Can't Create a New Team."
    #  return render_to_response('error.' + format, {'code': 200, 'description': error_message})

    if request.method != "POST":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    if ("teamname" in request.POST):
      if (request.POST["teamname"].strip() == ""):
        return render_to_response('error.' + format, {'code': 400, 'description': "Team Name is Empty."})
      teamname = request.POST["teamname"].strip().replace(' ', '_')
      num_first_challenge_id = -1
      if "first_challenge_team_id" in request.POST and request.POST["first_challenge_team_id"] != "None":
        num_first_challenge_id = int(request.POST["first_challenge_team_id"].strip())
      else:
        challenges = Challenge.objects.filter(event=event).order_by('number')
        num_first_challenge_id = challenges[0].id

      correct, result = api.team.create(event, teamname, num_first_challenge_id)

      if correct and format == 'html':
        url = "/gymkhana/event/" + str(event_id) + "/show/"
        return HttpResponseRedirect(url)
      elif correct:
        team = result
        first_challenge = FirstChallenge.objects.get(event=event, team=team)
        scoreboard = Scoreboard.objects.get(event=event, team=team)
        return render_to_response('create_team.' + format, {'code': 200, 'description': "ok", 'team': team, 'first_challenge': first_challenge, 'scoreboard': scoreboard})
      else:
        return render_to_response('error.' + format, {'code': 500, 'description': result})
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': "Missing \'teamname\' Parameter."})

@csrf_exempt
def team_edit(request, event_id, team_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': 'The User is not Authenticated.'})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = get_team(event, team_id)
    if correct:
      team = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    if "first_challenge_team_id" in request.GET:
      try:
        challenge_id = int(request.GET["first_challenge_team_id"].strip())
      except:
        return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Challenge."})
      correct, result = get_challenge(event, challenge_id)
      if correct:
        challenge = result
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': result})

      correct, result = api.team.edit_first_challenge(event, team, challenge)
      if correct:
        url = "/gymkhana/event/" + str(event_id) + "/show/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "Internal Error. " + result})
    elif "latitude" in request.GET and "longitude" in request.GET:
      correct, result = api.team.edit_position(team, float(request.GET["longitude"].strip()), float(request.GET["latitude"].strip()))
      if correct:
        return render_to_response('edit_team.' + format, {'code': 200, 'description': "ok"})
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "Internal Error. " + result})
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': "Missing Parameters."})

@csrf_exempt
def team_show(request, event_id, team_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})      

    correct, result = get_team(event, team_id)
    if correct:
      team = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': 'The User is not Authenticated.'})
    
    isAdmin = check_session_user_type(request)
    correct, message, team_members, first_challenge, scoreboard = api.team.show(event, team)

    if correct:
      if first_challenge != None:
        return render_to_response('show_team.' + format, {'code': 200, 'description': 'ok', 'event': event, 'team': team, 'team_members': team_members, 'num_team_members': len(team_members), 'first_challenge': first_challenge, 'scoreboard': scoreboard, 'isAdmin': isAdmin})
      elif first_challenge == None:
        return render_to_response('show_team.' + format, {'code': 200, 'description': 'ok', 'event': event, 'team': team, 'team_members': team_members, 'num_team_members': len(team_members), 'scoreboard': scoreboard, 'isAdmin': isAdmin})
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': "Internal Error. " + message})

def team_delete(request, event_id, team_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})      

    correct, result = get_team(event, team_id)
    if correct:
      team = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': 'The User is not Authenticated.'})

    if check_session_user_type(request) == False: # Si no es administrador, no puede eliminar equipos:
      return render_to_response('error.' + format, {'code': 200, 'description': "You Can't Delete a Team."})

    correct, manager = get_manager(event)
    correct, message = api.team.delete(team, manager)
    if correct:
      url = "/gymkhana/event/" + str(event_id) + "/show/"
      return HttpResponseRedirect(url)
    else:
      return render_to_response('error.' + format, {'code': 200, 'description': "Internal Error. " + message})

@csrf_exempt
def team_get_information_gymkhana(request, event_id, team_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': 'The User is not Authenticated.'})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})      

    correct, result = get_team(event, team_id)
    if correct:
      team = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    if "information" in request.GET:
      information_type = request.GET["information"].lower().strip()
      if information_type != "start_gymkhana" and information_type != "finish_gymkhana":
        error_message = "Incorrect Parameter \'information\' Value."
        return render_to_response('gymkhana_information.' + format, {'code': 400, 'description': error_message})
      else:
        if information_type == "finish_gymkhana":
          finished_objects = Finished.objects.filter(event=event, team=team)
          for finished_object in finished_objects:
            finished_object.delete()
          finished = Finished(event=event, team=team, is_finished=True)
          finished.save()
        correct, message, text, scoreboard = get_information_gymkhana(event, team, information_type)
        if correct:
          description = "Information Sent Successfully."
          return render_to_response('gymkhana_information.' + format, {'code': 200, 'description': description, 'informative_text': text, 'scoreboard': scoreboard, 'promotional_image_url': event.image})
    else:
      error_message = "Missing \'information\' Parameter."
      return render_to_response('gymkhana_information.' + format, {'code': 400, 'description': error_message})

@csrf_exempt
def team_member_has_team(request, event_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = get_team_member_by_user_id(event, request.user.id)
    print result
    if correct:
      team_member = result
    else:
      team_member = None

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    if team_member != None:
      team = team_member.team
      try:
        finished = Finished.objects.get(event=event,team=team)
        print finished.is_finished
        if finished.is_finished:
          team_members = TeamMember.objects.filter(event=event, team=team)
          for team_member in team_members:
            team_member.delete()
          return render_to_response('team_member_has_team.' + format, {'code': 200, 'description': "ok", "has_team": "false"})
        else:
          correct, message, current_challenge = get_current_challenge(event, team_member.team)
          correct, message, teams, first_challenges, scoreboards, finished_s, success = api.team.list(event)
          return render_to_response('team_member_has_team.' + format, {'code': 200, 'description': message, 'team': team, 'current_challenge': current_challenge, 'first_challenges': first_challenges, 'has_team': 'true', 'scoreboards': scoreboards})
      except:
        correct, message, current_challenge = get_current_challenge(event, team_member.team)
        correct, message, teams, first_challenges, scoreboards, finished_s, success = api.team.list(event)
        return render_to_response('team_member_has_team.' + format, {'code': 200, 'description': message, 'team': team, 'current_challenge': current_challenge, 'first_challenges': first_challenges, 'has_team': 'true', 'scoreboards': scoreboards})
    else:
      return render_to_response('team_member_has_team.' + format, {'code': 200, 'description': 'ok', "has_team": "false"})

@csrf_exempt
def team_member_previous_teams(request, event_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    correct, result = get_list_team_members()
    if correct:
      team_members = result
      challenges = Challenge.objects.filter(event=event).order_by('number')
      num_first_challenge_id = challenges[0].id
      return render_to_response('team_member_previous_teams.' + format, {'code': 200, 'description': "ok", 'team_members': team_members, 'user_id': request.user.id, 'user': request.user, 'num_first_challenge_id': num_first_challenge_id})
    else:
      team_members = None
      return render_to_response('error.' + format, {'code': 200, 'description': 'There Are No Previous Teams For This User.'})

@csrf_exempt
def team_member_create(request, event_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    if request.method != "POST":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    if "team_id" in request.POST and request.POST["team_id"] != 'None':
      correct, result = get_team(event, request.POST["team_id"].strip())
      if correct:
        team = result
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': result})
    else:
      error_message = "The participant group has not been indicated."
      return render_to_response('error.' + format, {'code': 400, 'description': error_message})

    if request.POST["action"].strip().lower() == "add": # el Add lo hace el administrador.
      #action = "add"
      try:
        first_name = request.POST["first_name"].strip()
        last_name = request.POST["last_name"].strip()
      except:
        return render_to_response('error.' + format, {'code': 400, 'description': "Missing Parameters"})
      correct, result = api.team_member.create(team, first_name, last_name)
      url = "/gymkhana/event/" + str(event_id) + "/show/"
      return HttpResponseRedirect(url)
    elif request.POST["action"].strip().lower() == "join": # el Join lo hace el propio usuario
      #action = "join"
      session_user_id = request.session["_auth_user_id"]
      team_id = int(request.POST["team_id"].strip())
      correct, result = api.team_member.join(team_id, session_user_id)
      if correct:
        url = "/gymkhana/event/" + str(event_id) + "/team/" + str(team.id) + "/show/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': result})
    else:
      error_message = "Invalid Parameter \'action\' Value."
      return render_to_response('error.' + format, {'code': 400, 'description': error_message})

@csrf_exempt
def team_member_delete(request, event_id, team_id, team_member_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})      

    correct, result = get_team(event, team_id)
    if correct:
      team = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    if check_session_user_type(request) == False: # Si no es administrador, no puede eliminar jugadores:
      return render_to_response('error.' + format, {'code': 200, 'description': "You Can't Delete a Team Member."})

    correct, result = get_team_member(team, team_member_id)
    if correct:
      team_member = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})
    
    correct, result = api.team_member.delete(team_member)
    if correct:
      url = "/gymkhana/event/" + str(event_id) + "/team/" + str(team_id) + "/show/"
      return HttpResponseRedirect(url)
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': "Internal Error. " + result})

@csrf_exempt
def response_edit(request, event_id, response_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})      

    if request.method != "GET": # REALMENTE DEBERIA SER UN POST!!!!!!!
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    try:
      team_id = request.GET["team_id"].strip()
    except:
      error_message = "Missing \'team_id\' Parameter."
      return render_to_response('error.' + format, {'code': 400, 'description': error_message})

    correct, result = get_team(event, team_id)
    if correct:
      team = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    try:
      response = team.responses.get(id=response_id)
    except:
      error_message = "Invalid Response Identifier."
      return render_to_response('error.' + format, {'code': 400, 'description': error_message})

    if "change_status" in request.GET:
      correct, message = api.response.edit(response, event, team, CORRECTION_FACTOR)
    else:
      error_message = "Missing \'change_status\' Parameter."
      return render_to_response('error.' + format, {'code': 400, 'description': error_message})

    response.save()
    #url = "/gymkhana/event/" + str(event_id) + "/response/list/"
    url = "/gymkhana/event/" + str(event_id) + "/monitoring/"
    return HttpResponseRedirect(url)

@csrf_exempt
def response_list(request, event_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})      

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    correct, result = api.team.list_order_by_id(event)
    if correct:
      return render_to_response('list_response.' + format, {'code': 200, 'description': 'ok', 'event': event, 'teams': result})
    else:
      return render_to_response('error.' + format, {'code': 500, 'description': "Internal Error. " + result})

@csrf_exempt
def response_delete(request, event_id, response_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})      

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    try:
      team_id = request.GET["team_id"].strip()
    except:
      error_message = "Missing \'team_id\' Parameter."
      return render_to_response('error.' + format, {'code': 400, 'description': error_message})

    correct, result = get_team(event, team_id)
    if correct:
      team = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    try:
      response = team.responses.get(id=response_id)
    except:
      error_message = "Invalid Response Identifier."
      return render_to_response('error.' + format, {'code': 400, 'description': error_message})

    correct, message = api.response.delete(response, event, team, CORRECTION_FACTOR)
    if correct:
      #url = "/gymkhana/event/" + str(event_id) + "/response/list/"
      url = "/gymkhana/event/" + str(event_id) + "/monitoring/"
      return HttpResponseRedirect(url)
    else:
      return render_to_response('error.' + format, {'code': 500, 'description': "Internal Error. " + message})

@csrf_exempt
def clue_buy(request, event_id, challenge_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})      

    correct, result = get_challenge(event, challenge_id)
    if correct:
      challenge = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if request.method != 'GET':
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})
    
    correct, result = get_team(event, request.GET['team_id'].strip())
    if correct:
      team = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = api.clue.buy(event, team, challenge)
    if correct == True:
      return render_to_response('show_clue.' + format, {'code': 200, 'description': "ok", 'clue': result})
    else:
      return render_to_response('show_clue.' + format, {'code': 200, 'description': result}) #"No More Clues For This Team And Challenge."

@csrf_exempt
def clue_show(request, event_id, challenge_id): # Muestra las pistas que ha comprado el equipo para una determinada prueba
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})      

    correct, result = get_challenge(event, challenge_id)
    if correct:
      challenge = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if request.method != 'GET':
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})
    
    correct, result = get_team(event, request.GET['team_id'].strip())
    if correct:
      team = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = api.clue.show(team, challenge)
    if correct:
      return render_to_response('show_clues.' + format, {'code': 200, 'description': "ok", 'acquired_clues': result, 'challenge': challenge})
    else: # Este equipo no ha comprado pistas para esta prueba (de este evento)
      return render_to_response('show_clues.' + format, {'code': 200, 'description': result}) # "You Have Not Got A Clue."

@csrf_exempt
def challenge_skip(request, event_id, challenge_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})      

    correct, result = get_challenge(event, challenge_id)
    if correct:
      challenge = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = get_team(event, request.GET['team_id'].strip())
    if correct:
      team = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if challenge.can_skip == False:
      return render_to_response('error.' + format, {'code': 400, 'description': "Challenge Can\'t Be Skipped"})

    correct, result = api.challenge.skip(team, challenge)
    if correct:
      skipped_challenge = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': "Internal Error. " + result})

    is_last_challenge, next_challenge_id = search_following_challenge(event, challenge, team, "Continue")

    description = "ok"
    message = "Correct Skip."
    return render_to_response('solution.' + format, {'code': 200, 'description': description, 'message': message, 'next_challenge_id': next_challenge_id, 'is_last_challenge': is_last_challenge})

@csrf_exempt
def skipped_challenge_list(request, event_id, team_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    if format == "html":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Format."})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = get_team(event, team_id)
    if correct:
      team = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})
    
    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    correct, result = api.challenge.skipped_list(team)
    if correct:
      return render_to_response('list_skipped_challenge.' + format, {'code': 200, 'description': 'ok', 'skipped_challenges': result, 'event': event})
    else:
      return render_to_response('error.' + format, {'code': 500, 'description': "Internal Error. " + result})

@csrf_exempt
def message_create(request, event_id):

    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if request.method == "GET":
      if format != "html":
        return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Format For a GET Method Request."})

      if not request.user.is_authenticated():
        if format == 'html':
          url = "/gymkhana/user/login/"
          return HttpResponseRedirect(url)
        else:
          return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

      if check_session_user_type(request) == False: # Si no es administrador, no le dejamos mandar mensajes desde interfaz web:
        return render_to_response('error.' + format, {'code': 200, 'description': "You Can't Sent a New Message."})
      
      correct, message, teams, first_challenges, scoreboards, finished_s, success = api.team.list(event)
      if not correct:
        return render_to_response('error.' + format, {'code': 500, 'description': "Internal Error. " + message})
      correct, manager = api.manager.show(event)
      if not correct:
        return render_to_response('error.' + format, {'code': 500, 'description': "Internal Error. " + message})
      return render_to_response('create_message.' + format, {'code': 200, 'description': "ok", 'event': event, 'teams': teams, 'manager': manager})

    elif request.method != "POST":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    if ("from_team_id" in request.POST or "from_manager_id" in request.POST) and ("to" in request.POST or "to_team_id" in request.POST) and "text" in request.POST:

      if "latitude" in request.POST and "longitude" in request.POST and "altitude" in request.POST:
        latitude = float(request.POST['latitude'].strip())
        longitude = float(request.POST['longitude'].strip())
        altitude = float(request.POST['altitude'].strip())
        position = Point(float(longitude), float(latitude), srid=4326)
      else:
        position = None
        altitude = None

      from_manager_id = -1
      from_team_id = -1
      to = -1
      to_team_id = -1
      to_manager_id = -1
      to_team = None
      manager = None
      correct, manager = api.manager.show(event)

      if "from_team_id" in request.POST:
        if request.POST["from_team_id"].strip() != "":
          from_team_id = int(request.POST["from_team_id"].strip())
      if "from_manager_id" in request.POST:
        if request.POST["from_manager_id"].strip() != "":
          from_manager_id = int(request.POST["from_manager_id"].strip())
      if (from_team_id == -1 and from_manager_id == -1) or (from_team_id != -1 and from_manager_id != -1):
        return render_to_response('error.' + format, {'code': 400, 'description': "Incorrect from_manager/team_id Parameters Values."})

      if "to" in request.POST:
        to = request.POST["to"].strip().lower()
        if to == "" or (to != "all" and to != "manager"):
          return render_to_response('error.' + format, {'code': 400, 'description': "Incorrect \'to\' Parameter Value."})
      if "to_team_id" in request.POST:
        to_team_id = int(request.POST["to_team_id"].strip())
        correct, result = get_team(event, to_team_id)
        if correct:
          to_team = result
        else:
          return render_to_response('error.' + format, {'code': 400, 'description': result})
      #if "to_manager_id" in request.POST:
      #  to_manager_id = int(request.POST["to_manager_id"].strip())
      #  correct, result = get_manager_by_id(event, to_manager_id)
      #  if correct:
      #    to_manager = result
      #  else:
      #    return render_to_response('error.' + format, {'code': 400, 'description': result})
      if to_team != None and (to != "" and (to == "all" or to == "manager")):
        return render_to_response('error.' + format, {'code': 400, 'description': "Incorrect to/to_team_id Parameters Values."})

      if request.POST["text"].strip() != "":
        text = request.POST["text"].strip()
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "Text Value Can\'t Be Empty."})

      correct, result = api.message.create(event, text, from_team_id, from_manager_id, to, to_team_id, to_manager_id, to_team, manager, position, altitude)
      if not correct:
        return render_to_response('error.' + format, {'code': 500, 'description': result})
      else:
        if format == "html":
          url = "/gymkhana/event/" + str(event.id) + "/monitoring/"
          return HttpResponseRedirect(url)
        else:
          return render_to_response('create_message.' + format, {'code': 200, 'description': "ok", 'event': event})
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': "Missing Parameters."})

@csrf_exempt
def message_list(request, event_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    if request.method == "html":
      return render_to_response('error.' + format, {'code': 400, 'description': 'Invalid Format.'})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})
    
    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    correct, result = api.message.list(event)
    if correct:
      messages = result
    else:
      return render_to_response('error.' + format, {'code': 500, 'description': "Internal Error. " + result})

    return render_to_response('list_message.' + format, {'code': 200, 'description': 'ok', 'messages': messages})

@csrf_exempt
def message_delete(request, event_id, message_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if format != "html":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Format."})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = get_message(event, message_id)
    if correct:
      message = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    isAdmin = check_session_user_type(request)
    if isAdmin == True:
      correct, result = api.message.delete(message)
      if not correct:
        return render_to_response('error.' + format, {'code': 400, 'description': "Internal Error. " + result})

      # De momento solo permito eliminar al manager y via html:
      url = "/gymkhana/event/" + str(event.id) + "/monitoring/"
      return HttpResponseRedirect(url)
    else:
      return render_to_response('error.' + format, {'code': 200, 'description': 'You Can\'t Delete A Message.'})

@csrf_exempt
def message_list_delete(request, event_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if format != "html":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Format."})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    isAdmin = check_session_user_type(request)
    if isAdmin == True:
      correct, result = api.message.delete_all(event)
      if not correct:
        return render_to_response('error.' + format, {'code': 400, 'description': "Internal Error. " + result})
      #event.message_set.all().delete()

      # De momento solo permito eliminar al manager y via html:
      url = "/gymkhana/event/" + str(event.id) + "/monitoring/"
      return HttpResponseRedirect(url)
    else:
      return render_to_response('error.' + format, {'code': 200, 'description': 'You Can\'t Delete All Messages.'})

@csrf_exempt
def number_team_sent_messages(request, event_id, team_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    if format == "html":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Format."})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = get_team(event, team_id)
    if correct:
      team = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    correct, result = api.message.list_by_team(event, team, "sent")
    if not correct:
      return render_to_response('error.' + format, {'code': 400, 'description': result})
    return render_to_response('num_messages.' + format, {'code': 200, 'description': 'ok', 'num_messages': len(result)})

@csrf_exempt
def number_team_inbox_messages(request, event_id, team_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    if format == "html":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Format."})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = get_team(event, team_id)
    if correct:
      team = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    correct, result = api.message.list_by_team(event, team, "inbox")
    if not correct:
      return render_to_response('error.' + format, {'code': 400, 'description': result})
    return render_to_response('num_messages.' + format, {'code': 200, 'description': 'ok', 'num_messages': len(result)})

@csrf_exempt
def team_show_sent_messages(request, event_id, team_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    if format == "html":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Format."})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = get_team(event, team_id)
    if correct:
      team = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    correct, result = api.message.list_by_team(event, team, "sent")
    if not correct:
      return render_to_response('error.' + format, {'code': 400, 'description': result})
    return render_to_response('list_message.' + format, {'code': 200, 'description': 'ok', 'messages': result})

@csrf_exempt
def team_show_inbox_messages(request, event_id, team_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    if format == "html":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Format."})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = get_team(event, team_id)
    if correct:
      team = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    correct, result = api.message.list_by_team(event, team, "inbox")
    if not correct:
      return render_to_response('error.' + format, {'code': 400, 'description': result})
    return render_to_response('list_message.' + format, {'code': 200, 'description': 'ok', 'messages': result})

@csrf_exempt
def message_reply(request, event_id, message_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = get_message(event, message_id)
    if correct:
      message = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if format == 'html' and check_logged_user(request) == False:
      url = "/gymkhana/user/login/"
      return HttpResponseRedirect(url)

    isAdmin = check_session_user_type(request)
    if isAdmin != True:
      return render_to_response('error.' + format, {'code': 200, 'description': 'You Can\'t Reply To A Message.'})

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    correct, message, to_manager, team_to_reply, from_manager, to_teams, text_to_reply = api.message.reply(message)
    if not correct:
      return render_to_response('error.' + format, {'code': 500, 'description': "Internal Error. " + message})

    correct, message, teams, first_challenges, scoreboards, finished_s, success = api.team.list(event)
    if not correct:
      return render_to_response('error.' + format, {'code': 500, 'description': "Internal Error. " + message})

    return render_to_response('create_message.' + format, {'code': 200, 'description': "ok", 'event': event, 'teams': teams, 'to_manager': to_manager, 'team_to_reply': team_to_reply, 'from_manager': from_manager, 'to_teams': to_teams, 'text_to_reply': text_to_reply})

@csrf_exempt
def overall_standings_show(request):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    if format == 'html' and check_logged_user(request) == False:
      url = "/gymkhana/user/login/"
      return HttpResponseRedirect(url)

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    if not "many" in request.GET:
      return render_to_response('error.' + format, {'code': 400, 'description': "Missing \'many\' Parameter."})

    overall_standings = get_overall_standings(request.GET["many"].strip())

    if len(overall_standings) == 0:
      return render_to_response('overall_standings.' + format, {'code': 200, 'description': "ok"})
    else:
      return render_to_response('overall_standings.' + format, {'code': 200, 'description': "ok", 'overall_standings': overall_standings})

@csrf_exempt
def my_standings_show(request):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    if format == 'html' and check_logged_user(request) == False:
      url = "/gymkhana/user/login/"
      return HttpResponseRedirect(url)

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    user = User.objects.get(pk=request.user.id)
    overall_standings = get_overall_standings(None)
    for i in range(len(overall_standings)):
      if overall_standings[i][0] == user.username:
        return render_to_response('my_standings.' + format, {'code': 200, 'description': "ok", 'user_standings': overall_standings[i], 'position': i+1})
    user_data = [user.username, 0, 0, LEVEL[0][0]]
    return render_to_response('my_standings.' + format, {'code': 200, 'description': "ok", 'user_standings': user_data, 'position': '0'})

@csrf_exempt
def my_standings_show2(request):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    if format == 'html' and check_logged_user(request) == False:
      url = "/gymkhana/user/login/"
      return HttpResponseRedirect(url)

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    user = User.objects.get(pk=request.user.id)
    team_members = []
    try:
      team_members = TeamMember.objects.get(user=user)
    except:
      pass

    user_data = []
    points = 0
    num_events = 0
    #if len(team_members) == 0:
    #  user.append(user.username)
    #  user.append(points)
    #  user.append(num_events)
    #else:
    for team_member in team_members:
      try:
        scoreboard = Scoreboard.objects.get(event=team_member.event, team=team_member.team)
        points = points + scoreboard.score
        num_events = num_events + 1
      except:
        pass
   
    user_data.append(user.username)
    user_data.append(points)
    user_data.append(num_events)

    found = 0
    for i in range(len(LEVEL)):
      if points == 0 and found == 0:
        user_data.append(LEVEL[0][0])
        found = 1
      if i == len(LEVEL)-1 and found == 0:
        if points > LEVEL[i][1]:
          user_data.append(LEVEL[i][0])
        else:
          user_data.append(LEVEL[i-1][0])
        found = 1
      elif points > LEVEL[i][1] and points <= LEVEL[i+1][1] and found == 0:
        #if points[index] <= LEVEL[i][1] and found == 0:
        user_data.append(LEVEL[i][0])
        found = 1

    return render_to_response('my_standings.' + format, {'code': 200, 'description': "ok", 'user_standings': user_data})

#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------

@csrf_exempt
def mobile_login(request):

    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if request.method == "GET":
      correct, managers = api.manager.list_all()
      if len(managers) == 0:
        manager = {'username': DEFAULT_MANAGER_USERNAME, 'password': DEFAULT_MANAGER_PASSWORD}
        correct, message = api_lgs.user.create_or_modify(manager, modify=False)
        if correct:
          user = Person.objects.get(id=message)
          default_manager = Manager(user=user)
          default_manager.save()
          return render_to_response('m_login.' + format, {'code': 200, 'description': 'ok'})
        else:
          return render_to_response('error.' + format, {'description': message})
      return render_to_response('m_login.' + format, {'code': 200, 'description': 'ok'})

    elif request.method == "POST":
      loginform = LoginForm(request.POST)
      id = loginform.login(request)
      if id:
        # Redirect to a success page.
        url = "/gymkhana/mobile/menu/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "Username and Password Do Not Match."})
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

@csrf_exempt
def mobile_menu(request):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/mobile/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    return render_to_response('m_menu.' + format, {'code': 200, 'description': 'ok'})

@csrf_exempt
def mobile_gymkhanas(request):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/mobile/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    correct, events = api.event.list_all()
    isAdmin = check_session_user_type(request)
    correct, managers = api.manager.list_all()
    if len(events) == 0:
      return render_to_response('m_gymkhanas.' + format, {'code': 200, 'description': 'There Are No Events', 'isAdmin': isAdmin, 'managers': managers})
    else:
      return render_to_response('m_gymkhanas.' + format, {'code': 200, 'description': 'ok', 'events': events, 'isAdmin': isAdmin, 'managers': managers})

@csrf_exempt
def new_user(request):

    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    is_admin = False
    correct, managers = api.manager.list_all()
    if correct:
      for manager in managers:
        if request.user.username == manager.user.username:
          is_admin = True

    if request.method == "GET":
      return render_to_response('m_register.' + format, {'code': 200, 'description': 'ok', 'logged_user_is_admin': is_admin })

    elif request.method == "POST":
      if ("password" in request.POST) and ("username" in request.POST) and ("first_name" in request.POST) and ("last_name" in request.POST):
        user = {'username': request.POST["username"].strip(), 'password': request.POST["password"],
                'first_name': request.POST["first_name"].strip(), 'last_name': request.POST["last_name"].strip()}
        correct, message = api_lgs.user.create_or_modify(user, modify=False)

        if is_admin:
          if "is_manager" in request.POST and request.POST['is_manager'] == 'True':
            new_user = Person.objects.get(id=message)
            new_manager = Manager(user=new_user)
            new_manager.save()

        if correct:
          url = "/gymkhana/mobile/login/"
          return HttpResponseRedirect(url)
        else:
          return render_to_response('error.' + format, {'code': 500, 'description': message})
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "Missing Parameters."})
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

@csrf_exempt
def list_teams(request, event_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/mobile/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = get_team_member_by_user_id(event, request.user.id)
    if correct:
      team_member = result
    else:
      team_member = None

    correct, message, teams, first_challenges, scoreboards, finished_s, success = api.team.list(event)
    if not correct:
      return render_to_response('error.' + format, {'code': 400, 'description': "Internal Error. " + message})

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    if team_member != None:
      team = team_member.team
      try:
        finished = Finished.objects.get(event=event,team=team)
        if finished.is_finished:
          team_members = TeamMember.objects.filter(event=event, team=team)
          for team_member in team_members:
            team_member.delete()
          return render_to_response('list_teams.' + format, {'code': 200, 'description': "ok", 'event': event, 'teams': teams})
        
        else:
          correct, message, current_challenge = get_current_challenge(event, team_member.team)
          correct, message, teams, first_challenges, scoreboards, finished_s, success = api.team.list(event)
	  url = "/gymkhana/event/" + str(event.id) + "/team/" + str(team.id) + "/challenge/" + str(current_challenge.id) + "/event_show/"
	  return HttpResponseRedirect(url)
      except:
        correct, message, current_challenge = get_current_challenge(event, team_member.team)
        correct, message, teams, first_challenges, scoreboards, finished_s, success = api.team.list(event)
        return render_to_response('list_teams.' + format, {'code': 200, 'description': message, 'event': event, 'teams': teams})
    
    
    else:  # se acaba de meter, no tiene equipo
      return render_to_response('list_teams.' + format, {'code': 200, 'description': 'ok', 'event': event, 'teams': teams})

@csrf_exempt
def start(request, event_id, team_id):

    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if format != "html":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Format."})

    if not request.user.is_authenticated():
      url = "/gymkhana/mobile/login/"
      return HttpResponseRedirect(url)

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    correct, result = get_team(event, team_id)
    if correct:
      team = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    try:
      objetos = Finished.objects.all()
      finished = Finished.objects.get(event=event, team=team)
      if finished.is_finished: # Si el team ha acabado la gymkhana y quiere volverla a hacer
        finished.delete()
        team_members = TeamMember.objects.filter(event=event, team=team)
        for team_member in team_members:
          team_member.delete()
        teams = event.team_set.all()
        for team_1 in teams:
          if team_1 == team:
            #team_1.unjoin()
            correct, message = api.team.unjoin(event, team)
            team.responses.delete()
        correct, message, first_challenge = api.team.join_to_event(event, team)
        finished = Finished(event=event, team=team, is_finished=False)
        finished.save()
#      else:
#        print 'else finish'
#        print request.user.id
#        correct, message = api.team_member.create_by_user_id(event, team, request.user.id)
#        print message
    except:
      finished = Finished(event=event, team=team, is_finished=False)
      finished.save()
      correct, message, first_challenge = api.team.join_to_event(event, team)

    first_challenge = FirstChallenge.objects.get(event=event, team=team)
    correct, message = api.team_member.create_by_user_id(event, team, request.user.id)
    return render_to_response('start.' + format, {'code': 200, 'description': "ok", 'team_id':team_id, 'event':event, 'first_challenge_id': first_challenge.first_challenge.id})


@csrf_exempt
def mobile_event_show(request, event_id, team_id, challenge_id):

    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/mobile/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = get_team(event, team_id)
    if correct:
      team = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = get_challenge(event, challenge_id)
    if correct:
      challenge = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    num_clues = len(Clue.objects.filter(challenge=challenge))
    all_teams = event.team_set.all()
    teams = []
    for a_team in all_teams:
      if a_team.id != int(team_id):
        teams.append(a_team)
    try:
      manager = Manager.objects.get(events__id=event.id)
    except:
      manager = None

#    correct, result = api.team.getParameters(event.id, team.id)
#    if correct:
#      parameters = result[0]
#    else:
#      parameters = Parameters(event_id=event_id, team_id=team_id, time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), length=0)

    if request.method == "GET":
      description = "Challenge Correctly Sent."
      if challenge.challenge_type == GEOLOCATION_CHALLENGE:
        return render_to_response('event.' + format, {'code': 200, 'description': description, 'event_id': event.id, 'team': team, 'challenge_id':challenge_id, 'challenge': challenge.challenge, 'max_score': challenge.max_score, 'challenge_type': challenge.challenge_type, 'augmented_reality': challenge.augmented_reality, 'can_skip': challenge.can_skip, 'number': challenge.number, 'target_place': challenge.target_place, 'distance_to_target_place': challenge.distance_to_target_place, 'mark_place': challenge.mark_place, 'num_clues': num_clues, 'picture': challenge.picture, 'teams':teams, 'manager':manager})
#'parameters':parameters})


      return render_to_response('event.' + format, {'code': 200, 'description': description, 'event_id': event.id, 'team': team, 'challenge_id':challenge_id, 'challenge': challenge.challenge, 'max_score': challenge.max_score, 'challenge_type': challenge.challenge_type, 'augmented_reality': challenge.augmented_reality, 'can_skip': challenge.can_skip, 'number': challenge.number, 'num_clues': num_clues, 'picture': challenge.picture, 'teams':teams, 'manager':manager})
#, 'parameters':parameters})

    elif request.method == "POST":

      if "latitude" in request.POST and "longitude" in request.POST:
	if request.POST['latitude'] != '' or request.POST['longitude'] != '':
          latitude = float(request.POST['latitude'].strip())
          longitude = float(request.POST['longitude'].strip())
          altitude = 0.0
          position = Point(float(longitude), float(latitude), srid=4326)

        else:
	  latitude = 40.416748
	  longitude = -3.703408
	  altitude = 0.0
	  position = Point(float(longitude), float(latitude), srid=4326)

      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "Missing \'latitude\'/\'longitude\'/\'altitude\' Parameter/s."})

#      correct, result = api.team.delete_parameters(event_id, team_id)
#      date = request.POST['date'].strip()
#      length = request.POST['length_messages'].strip()
#      correct, parameters = api.team.save_parameters(event_id, team_id, date, length)

      response_to_challenge = None
      distance_difference = -1

      if challenge.challenge_type == TEXTUAL_CHALLENGE and 'answer' in request.POST:
        response_to_challenge = request.POST['answer'].strip()
      elif challenge.challenge_type == PHOTO_CHALLENGE:
        correct, result = read_photo(request)
        if correct:
          response_to_challenge = result
        else:
          return render_to_response('error.' + format, {'code': 400, 'description': result})
      elif challenge.challenge_type == GEOLOCATION_CHALLENGE:
        if "distance_difference" in request.POST:
          distance_difference = float(request.POST['distance_difference'].strip())
        else:
          return render_to_response('error.' + format, {'code': 400, 'description': "Missing \'distance_difference\' Parameter/s."})
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "Missing \'response\' or \'photo\' Parameter."})

      correct, response, message = api.challenge.respond(event, team, challenge, response_to_challenge, CORRECTION_FACTOR, position, altitude, distance_difference)

      if message == "Continue":
        if challenge.can_skip != False:
	  correct, result = api.challenge.skipped_list(team)
	  if correct:
	    skipped_challenges = result
	  else:
	    skipped_challenges = None

          if skipped_challenges != None:
	    for skipped in skipped_challenges:
	      if ( skipped.challenge.id == int(challenge_id)):
                correct = api.challenge.delete_skip_challenge(team, challenge)

        is_last_challenge, next_challenge_id = search_following_challenge(event, challenge, team, message)
        if (is_last_challenge == 'True') or (int(next_challenge_id) == int(challenge_id)):
          url = "/gymkhana/event/" + str(event.id) + "/team/" + str(team.id) + "/end/"
          return HttpResponseRedirect(url)
        else:
          url = "/gymkhana/event/" + str(event.id) + "/team/" + str(team.id) + "/challenge/" + str(next_challenge_id) + "/event_show/"
          return HttpResponseRedirect(url)
      else:
        return render_to_response('event.' + format, {'code': 200, 'description': response, 'event_id': event.id, 'team': team, 'challenge_id':challenge_id, 'challenge': challenge.challenge, 'max_score': challenge.max_score, 'challenge_type': challenge.challenge_type, 'augmented_reality': challenge.augmented_reality, 'can_skip': challenge.can_skip, 'number': challenge.number, 'num_clues': num_clues, 'picture': challenge.picture, 'repeat':True, 'teams':teams, 'manager': manager})
#, 'parameters':parameters})

@csrf_exempt
def end(request, event_id, team_id):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/mobile/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': 'The User is not Authenticated.'})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})      

    correct, result = get_team(event, team_id)
    if correct:
      team = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    finished_objects = Finished.objects.filter(event=event, team=team)
    for finished_object in finished_objects:
      finished_object.delete()
    finished = Finished(event=event, team=team, is_finished=True)
    finished.save()

    information_type = "finish_gymkhana"
    correct, message, text, scoreboard = get_information_gymkhana(event, team, information_type)
    if correct:
      return render_to_response('end.' + format, {'code': 200, 'description': message, 'event_title':event.title, 'goodbye_text': text, 'scoreboard': scoreboard, 'promotional_image_url': event.image})

@csrf_exempt
def show_list_clues(request, event_id, team_id, challenge_id):

    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/mobile/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = get_team(event, team_id)
    if correct:
      team = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = get_challenge(event, challenge_id)
    if correct:
      challenge = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    clues = Clue.objects.filter(challenge=challenge)
    return render_to_response('dialogs/showClues.' + format, {'code': 200, 'description':'ok', 'clues': clues, 'event_id': event.id, 'team_id': team.id, 'challenge_id':challenge_id})

@csrf_exempt
def get_clue(request, event_id, team_id, challenge_id):

    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/mobile/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = get_team(event, team_id)
    if correct:
      team = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = get_challenge(event, challenge_id)
    if correct:
      challenge = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = api.clue.buy(event, team, challenge)
    if correct == True:
      return render_to_response('dialogs/getClue.' + format, {'code': 200, 'description': "ok", 'correct':correct, 'clue': result, 'event_id': event.id, 'team_id': team.id, 'challenge_id':challenge_id})
    else:
      return render_to_response('dialogs/getClue.' + format, {'code': 200, 'description': result, 'correct':correct}) #"No More Clues For This Team And Challenge."

@csrf_exempt
def list_clues(request, event_id, team_id, challenge_id):

    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/mobile/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = get_team(event, team_id)
    if correct:
      team = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = get_challenge(event, challenge_id)
    if correct:
      challenge = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    all_acquired_clues = AcquiredClue.objects.filter(team=team)
    acquired_clues = []
    for clues in all_acquired_clues:
      if clues.clue.challenge.id == int(challenge_id):
        acquired_clues.append(clues)
    
    return render_to_response('dialogs/list_clues.' + format, {'code': 200, 'description':'ok', 'clues': acquired_clues})

@csrf_exempt
def ask_skip (request, event_id, team_id, challenge_id):

    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/mobile/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})      

    correct, result = get_challenge(event, challenge_id)
    if correct:
      challenge = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = get_team(event, team_id)
    if correct:
      team = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    if challenge.can_skip == False:
      return render_to_response('dialogs/skip.' + format, {'code': 200, 'description': "Challenge Can\'t Be Skipped", "is_skipped" : challenge.can_skip})

    is_last_challenge, next_challenge_id = search_following_challenge(event, challenge, team, "Continue")
    is_last_challenge = False
    if int(next_challenge_id) == int(challenge_id):
      is_last_challenge = True
      return render_to_response('dialogs/skip.' + format, {'code':200, 'description': 'ok', 'is_last_challenge': is_last_challenge, "is_skipped" : challenge.can_skip})

    return render_to_response('dialogs/skip.' + format, {'code':200, 'description': 'ok', 'is_last_challenge': is_last_challenge, "is_skipped" : challenge.can_skip,  'event_id': event.id, 'team_id': team.id, 'challenge_id':challenge_id})


@csrf_exempt
def skip_challenge (request, event_id, team_id, challenge_id):

    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/mobile/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = get_challenge(event, challenge_id)
    if correct:
      challenge = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = get_team(event, team_id)
    if correct:
      team = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = api.challenge.skip(team, challenge)
    if correct:
      skipped_challenge = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': "Internal Error. " + result})

    is_last_challenge, next_challenge_id = search_following_challenge(event, challenge, team, "Continue")

    url = "/gymkhana/event/" + str(event_id) + "/team/" + str(team_id) + "/challenge/" + str(next_challenge_id) + "/event_show/"
    return HttpResponseRedirect(url)

@csrf_exempt
def skip_list (request, event_id, team_id, challenge_id):

    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/mobile/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = get_team(event, team_id)
    if correct:
      team = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = api.challenge.skipped_list(team)
    skipped_list = []
    for skipped in result:
      if skipped.challenge.id != int(challenge_id):
	skipped_list.append(skipped)

    if correct:
      return render_to_response('dialogs/retry.' + format, {'code': 200, 'description': 'ok', 'skipped_challenges': skipped_list, 'event': event, 'team_id':team_id, 'challenge_id':challenge_id})
    else:
      return render_to_response('error.' + format, {'code': 500, 'description': "Internal Error. " + result})

@csrf_exempt
def process_message(request, event_id, team_id):

    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = get_team(event, team_id)
    if correct:
      team = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

#    if "latitude2" in request.POST and "longitude2" in request.POST:
#      latitude = float(request.POST['latitude2'].strip())
#      longitude = float(request.POST['longitude2'].strip())
#      altitude = 0.0
#      position = Point(float(longitude), float(latitude), srid=4326)
#    else:
      return render_to_response('error.' + format, {'code': 400, 'description': "Missing \'latitude\'/\'longitude\'/\'altitude\' Parameter/s."})

#    correct, result = api.team.delete_parameters(event_id, team_id)
#    date = request.POST['date'].strip()
#    length = request.POST['length_messages'].strip()
#    correct, parameters = api.team.save_parameters(event_id, team_id, date, length)

    position = None
    altitude = None

    from_manager_id = -1
    to = -1
    to_team_id = -1
    to_manager_id = -1
    to_team = None
    manager = None
    correct, manager = api.manager.show(event)

    from_team_id = int(team_id)
    destin = request.POST["to"].strip().lower()     
    if destin != 'all' and destin != 'manager':
      to_team_id = int(destin)
      correct, result = get_team(event, to_team_id)
      if correct:
        to_team = result
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': result})
    if destin == "manager":
      to = destin
    if destin == "all":
      to = destin

    text = request.POST['message'].strip()

    correct, result = api.message.create(event, text, from_team_id, from_manager_id, to, to_team_id, to_manager_id, to_team, manager, position, altitude)
    if not correct:
      return render_to_response('error.' + format, {'code': 500, 'description': result})
    else:
      correct, message, current_challenge = get_current_challenge(event, team)
      url = "/gymkhana/event/" + str(event.id) + "/team/" + team_id + "/challenge/" + str(current_challenge.id) + "/event_show/"
      return HttpResponseRedirect(url)

@csrf_exempt
def show_messages(request, event_id, team_id):

    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    correct, result = get_event(event_id)
    if correct:
      event = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    correct, result = get_team(event, team_id)
    if correct:
      team = result
    else:
      return render_to_response('error.' + format, {'code': 400, 'description': result})

    option = str(request.GET["option"].strip())

    correct, result = api.message.list_by_team(event, team, option)
    if not correct:
      return render_to_response('error.' + format, {'code': 400, 'description': result})
    messages = result
    correct, message, current_challenge = get_current_challenge(event, team)

    return render_to_response('show_messages.' + format, {'code': 200, 'description': 'ok', 'messages': messages, 'challenge': current_challenge, 'event_id':event_id, 'team_id':team_id, 'option': option})

@csrf_exempt
def parameters (request, event_id, team_id):

    if request.method == "GET":
      correct, result = api.team.getParameters(event_id, team_id)
      if correct:
        parameters = result[0]
      else:
        parameters = Parameters(event_id=event_id, team_id=team_id, time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), length=0)      
      return render_to_response('parameters.json', {'code': 200, 'description': 'ok', 'parameters':parameters, 'date':parameters.time, 'length':parameters.length})

    if request.method == "POST":
      length = request.GET["length"].strip()
      date = request.GET["date"].strip()
      correct, result = api.team.delete_parameters(event_id, team_id)
      correct, parameters = api.team.save_parameters(event_id, team_id, date, length)
      return render_to_response('parameters.json', {'code': 200, 'description': 'ok'})

@csrf_exempt
def show_ranking(request):
    correct, result = check_format(request, DEFAULT_FORMAT)
    if correct:
      format = result
    else:
      return render_to_response('error.' + DEFAULT_FORMAT, {'code': 400, 'description': result})

    if not request.user.is_authenticated():
      if format == 'html':
        url = "/gymkhana/user/login/"
        return HttpResponseRedirect(url)
      else:
        return render_to_response('error.' + format, {'code': 400, 'description': "The User is not Authenticated."})

    if format == 'html' and check_logged_user(request) == False:
      url = "/gymkhana/mobile/login/"
      return HttpResponseRedirect(url)

    if request.method != "GET":
      return render_to_response('error.' + format, {'code': 400, 'description': "Invalid Method Request."})

    position='0'
    user = User.objects.get(pk=request.user.id)
    user_data = [user.username, 0, 0, LEVEL[0][0]]
    overall_standings = get_overall_standings(None)
    for i in range(len(overall_standings)):
      if overall_standings[i][0] == user.username:
        position = i+1
        user_data = overall_standings[i]

    overall_standings2 = get_overall_standings(10)
    return render_to_response('rankings.' + format, {'code': 200, 'description': "ok", 'overall_standings': overall_standings2, 'user_standings':user_data, 'position':position})

@csrf_exempt
def mobile_logout(request):
    logout(request)
    # Redirect to a success page.
    url = "/gymkhana/mobile/login/"
    return HttpResponseRedirect(url)
