# -*- coding: UTF-8 -*-


from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from datetime import datetime

from django.contrib.auth import authenticate, login, logout

from django.contrib.gis.geos import Point


from social.core import api as api_lgs
from social.rest.forms import LoginForm
from social.core.models import *
from apps.explohyperfiction.core import utils
from apps.explohyperfiction.models import *
from apps.explohyperfiction.core import api
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt

from time import sleep

def home(request):
    to_json = {
        "status": "OK"
    }
    return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')


@csrf_exempt
def login(request):
    if request.method=="POST":
        loginform = LoginForm(request.POST)
        if loginform.login(request):
            to_json={
                "status":"OK"
            }
        else:
            to_json= {
                "status":"ERROR",
                "message":"Username or password incorrect"
            }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')

def events_all(request):
    if not request.user.is_authenticated():
        to_json={
            "status":"ERROR",
            "message":"You are not authenticated"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    person=Person.objects.get(id=request.session["_auth_user_id"])
    if request.method !="GET":
        to_json={
            "status":"ERROR",
            "message":"Forbidden http method"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    if not Player.objects.filter(person=person):
        to_json={
            "status":"ERROR",
            "message":"You are not member of Explohyperfiction"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    player=Player.objects.get(person=person)
    events=Event.objects.filter(group__in=player.groups.all(),active=True)
    if len(events)==0:
        to_json={
            "status":"ERROR",
            "message":"There are not events to show"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    eventsJSON=[]
    for event in events:
        eventJSON={
            "name":event.name,
            "description":event.description,
            "id":str(event.id),
            "manager":event.manager.person.username,
            "date":str(event.date)
        }
        eventsJSON.append(eventJSON)
    to_json={
        "status":"OK",
        "events":eventsJSON
    }
    return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')

def events_started(request):
    if not request.user.is_authenticated():
        to_json={
            "status":"ERROR",
            "message":"You are not authenticated"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    person=Person.objects.get(id=request.session["_auth_user_id"])
    if request.method !="GET":
        to_json={
            "status":"ERROR",
            "message":"Forbidden http method"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    if not Player.objects.filter(person=person):
        to_json={
            "status":"ERROR",
            "message":"You are not member of Explohyperfiction"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    player=Player.objects.get(person=person)
    challenges=Challenge.objects.filter(user=player,finish=False)
    if len(challenges)==0:
        to_json={
            "status":"ERROR",
            "message":"There are not challenges to continue"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    eventsJSON=[]
    for challenge in challenges:
        eventJSON={
            "name":challenge.event.name,
            "description":challenge.event.description,
            "id":str(challenge.event.id),
            "manager":challenge.event.manager.person.username,
            "date":str(challenge.event.date)
        }
        eventsJSON.append(eventJSON)
    to_json={
        "status":"OK",
        "events":eventsJSON
    }
    return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')

def results_all(request):
    if not request.user.is_authenticated():
        to_json={
            "status":"ERROR",
            "message":"You are not authenticated"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    person=Person.objects.get(id=request.session["_auth_user_id"])
    if request.method !="GET":
        to_json={
            "status":"ERROR",
            "message":"Forbidden http method"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    if not Player.objects.filter(person=person):
        to_json={
            "status":"ERROR",
            "message":"You are not member of Explohyperfiction"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    player=Player.objects.get(person=person)
    challenges=Challenge.objects.filter(user=player,finish=True)
    if len(challenges)==0:
        to_json={
            "status":"ERROR",
            "message":"There are not results to show"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    challengesJSON=[]
    for challenge in challenges:
        challengeJSON={
            "id":str(challenge.id),
            "name":challenge.event.name,
            "dateStart":str(challenge.date),
            "dateFinish":str(challenge.date_finish)
        }
        challengesJSON.append(challengeJSON)
    to_json={
        "status":"OK",
        "challenges":challengesJSON
    }
    return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
  

def event_profile(request, id_event):
    if not request.user.is_authenticated():
        to_json={
            "status":"ERROR",
            "message":"You are not authenticated"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    person=Person.objects.get(id=request.session["_auth_user_id"])
    if request.method !="GET":
        to_json={
            "status":"ERROR",
            "message":"Forbidden http method"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    if not Player.objects.filter(person=person):
        to_json={
            "status":"ERROR",
            "message":"You are not member of Explohyperfiction"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    if not Event.objects.filter(id=int(id_event), active=True):
        to_json={
            "status":"ERROR",
            "message":"The event doesn't exists"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    player=Player.objects.get(person=person)
    event=Event.objects.get(id=int(id_event))
    eventJSON={
            "name":event.name,
            "description":event.description,
            "id":str(event.id),
            "manager":event.manager.person.username,
            "date":str(event.date)
    }
    to_json={
        "status":"OK",
        "event":eventJSON
    }
    if Challenge.objects.filter(event=event,user=player, finish=False):
        to_json["started"]="true"
    else:
        to_json["started"]="false"
                                                           
    return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
 
 
def challenge_start(request,id_event):   
    if not request.user.is_authenticated():
        to_json={
            "status":"ERROR",
            "message":"You are not authenticated"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    person=Person.objects.get(id=request.session["_auth_user_id"])
    if request.method !="GET":
        to_json={
            "status":"ERROR",
            "message":"Forbidden http method"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    if not Player.objects.filter(person=person):
        to_json={
            "status":"ERROR",
            "message":"You are not member of Explohyperfiction"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    if not Event.objects.filter(id=int(id_event), active=True):
        to_json={
            "status":"ERROR",
            "message":"The event doesn't exists"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    player=Player.objects.get(person=person)
    event=Event.objects.get(id=int(id_event))
    if Challenge.objects.filter(event=event,user=player, finish=False):
        to_json={
            "status":"ERROR",
            "message":"You have already started this event"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    challenge=api.challenge.create(event,player,True)
    question=Question.objects.filter(event=event, level=1)[0]
    to_json={
        "status":"OK",
        "challenge_id":str(challenge.id),
        "next_question":str(question.id)
    }                  
    return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')

def challenge_continue(request,id_event):   
    if not request.user.is_authenticated():
        to_json={
            "status":"ERROR",
            "message":"You are not authenticated"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    person=Person.objects.get(id=request.session["_auth_user_id"])
    if request.method !="GET":
        to_json={
            "status":"ERROR",
            "message":"Forbidden http method"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    if not Player.objects.filter(person=person):
        to_json={
            "status":"ERROR",
            "message":"You are not member of Explohyperfiction"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    if not Event.objects.filter(id=int(id_event), active=True):
        to_json={
            "status":"ERROR",
            "message":"The event doesn't exists"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    player=Player.objects.get(person=person)
    event=Event.objects.get(id=int(id_event))
    if not Challenge.objects.filter(event=event,user=player, finish=False):
        to_json={
            "status":"ERROR",
            "message":"You have already started this event"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    challenge=Challenge.objects.filter(event=event,user=player,finish=False)[0]
    responses=Responses.objects.filter(challenge=challenge)
    if len(responses)==0:
        question=Question.objects.filter(event=event, level=1)[0]
        to_json={
        "status":"OK",
        "challenge_id":str(challenge.id),
        "next_question":str(question.id)
        }        
    else:
        to_json={
           "status":"OK",
           "challenge_id":str(challenge.id),
           "next_question":str(responses.order_by('-date')[0].answer.next)
        }                  
    return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')


def challenge_answer(request, id_challenge, id_question, id_answer):
    if not request.user.is_authenticated():
        to_json={
            "status":"ERROR",
            "message":"You are not authenticated"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    person=Person.objects.get(id=request.session["_auth_user_id"])
    if request.method !="GET":
        to_json={
            "status":"ERROR",
            "message":"Forbidden http method"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    if not Player.objects.filter(person=person):
        to_json={
            "status":"ERROR",
            "message":"You are not member of Explohyperfiction"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    if not Challenge.objects.filter(id=int(id_challenge)):
        to_json={
            "status":"ERROR",
            "message":"The challenge doesn't exists"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    player=Player.objects.get(person=person)
    challenge=Challenge.objects.get(id=int(id_challenge))
    if not Question.objects.filter(id=int(id_question)):
        print "Hola"
        to_json={
            "status":"ERROR",
            "message":"The question doesn't exists"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    question=Question.objects.get(id=int(id_question))
    if not question.event == challenge.event:
        to_json={
            "status":"ERROR",
            "message":"The event doesnt have this question"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    if not Answer.objects.filter(id=int(id_answer)):
        to_json={
            "status":"ERROR",
            "message":"The answer doesn't exists"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    answer=Answer.objects.get(id=int(id_answer))
    if not question == answer.question:
        to_json={
            "status":"ERROR",
            "message":"The question doesn't exists"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    api.responses.create(challenge,question,answer)
    to_json={
        "status":"OK",
        "challenge_id":str(challenge.id),
        "next_question":str(answer.next)
    } 
    if not answer.next:
        challenge.finish=True
        challenge.date_finish=datetime.now()
        challenge.save()                 
    return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
 
 
def challenge_summary(request, id_challenge):
    if not request.user.is_authenticated():
        to_json={
            "status":"ERROR",
            "message":"You are not authenticated"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    person=Person.objects.get(id=request.session["_auth_user_id"])
    if request.method !="GET":
        to_json={
            "status":"ERROR",
            "message":"Forbidden http method"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    if not Player.objects.filter(person=person):
        to_json={
            "status":"ERROR",
            "message":"You are not member of Explohyperfiction"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    if not Challenge.objects.filter(id=int(id_challenge)):
        to_json={
            "status":"ERROR",
            "message":"The challenge doesn't exists"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    player=Player.objects.get(person=person)
    challenge=Challenge.objects.get(id=int(id_challenge))
    summaries=Responses.objects.filter(challenge=challenge)
    summariesJSON=[]
    for summary in summaries:
        summaryJSON={
            "date":str(summary.date),
            "question":summary.question.text,
            "answer":summary.answer.text,
            "message":summary.answer.message
        }  
        summariesJSON.append(summaryJSON) 
    challengeJSON={
            "id":str(challenge.id),
            "name":challenge.event.name,
            "dateStart":str(challenge.date),
            "dateFinish":str(challenge.date_finish)
            } 
    to_json={
        "status":"OK",
        "challenge":challengeJSON,
        "summaries":summariesJSON
    } 
    return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
 
def challenge_question(request, id_challenge,id_question):
    if not request.user.is_authenticated():
        to_json={
            "status":"ERROR",
            "message":"You are not authenticated"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    person=Person.objects.get(id=request.session["_auth_user_id"])
    if request.method !="GET":
        to_json={
            "status":"ERROR",
            "message":"Forbidden http method"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    if not Player.objects.filter(person=person):
        to_json={
            "status":"ERROR",
            "message":"You are not member of Explohyperfiction"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    if not Challenge.objects.filter(id=int(id_challenge)):
        to_json={
            "status":"ERROR",
            "message":"The challenge doesn't exists"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    player=Player.objects.get(person=person)
    challenge=Challenge.objects.get(id=int(id_challenge))
    if not Question.objects.filter(id=int(id_question)):
        to_json={
            "status":"ERROR",
            "message":"The question doesn't exists"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    question=Question.objects.get(id=int(id_question))
    if not question.event == challenge.event:
        to_json={
            "status":"ERROR",
            "message":"The question doesn't exists"
        }
        return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    
    answers=Answer.objects.filter(question=question)
    answersJSON=[]
    for answer in answers:
        answerJSON= {
            "answer":answer.text,
            "id":str(answer.id)
        }
        if not answer.next:
            answerJSON["end"]=True
        answersJSON.append(answerJSON)
    to_json={
    "status":"OK",
    "id":str(question.id),
    "question":question.text,
    "answers":answersJSON,
    "challenge":str(challenge.id)
    }
    if question.qr:
        to_json["qr"]=True
    return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    
@csrf_exempt
def set_position(request):
    print request.POST
    person=Person.objects.get(id=request.session["_auth_user_id"])
    player=Player.objects.get(person=person)
    latitude = float(request.POST["latitude"])
    longitude = float(request.POST["longitude"])
    altitude = float(request.POST["altitude"])
    print latitude, longitude, altitude
    if (latitude!=0) and (longitude !=0) and (altitude!=0):
        position= Point(longitude, latitude,srid=4326)
        player.person.position=position
        player.person.altitude=altitude
        player.person.save()
    print latitude
    print longitude
    print altitude
    return HttpResponse()




