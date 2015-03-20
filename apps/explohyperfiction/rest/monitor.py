# -*- coding: UTF-8 -*-


from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from datetime import datetime

from django.contrib.auth import authenticate, login, logout

from django.contrib.gis.geos import Point

from django.utils import simplejson
from social.core import api as api_lgs
from social.rest.forms import LoginForm
from social.core.models import *
from apps.explohyperfiction.core import utils
from apps.explohyperfiction.models import *
from apps.explohyperfiction.core import api

def main(request):
    if not request.user.is_authenticated():
        data={"message": "You are not autheticated in LGS"}
        return render_to_response("explohyperfiction_error.html", data)
    person=Person.objects.get(id=request.session["_auth_user_id"])
    if request.method !="GET":
        data={"message": "Forbidden"}
        return render_to_response("explohyperfiction_error.html", data)
    if not Player.objects.filter(person=person):
        data={"message": "You are not member of ExploHyperfiction"}
        return render_to_response("explohyperfiction_error.html", data)
    player=Player.objects.get(person=person)
    if not player.is_manager:
        data={"message": "You must be manager"}
        return render_to_response("explohyperfiction_error.html", data)
    data={"player":player, "login":True, "number_of_notices":len(SystemMessage.objects.filter(to=player)), "number_of_petitions":len(Petition.objects.all())}
    data["events"]=Event.objects.filter(manager=player,active=True).order_by('name')
    template=get_template("explohyperfiction_monitoring.html")
    return HttpResponse(template.render(RequestContext(request,data)))


def event(request,id_event):
    if not request.user.is_authenticated():
        data={"message": "You are not autheticated in LGS"}
        return render_to_response("explohyperfiction_error.html", data)
    person=Person.objects.get(id=request.session["_auth_user_id"])
    if request.method !="GET":
        data={"message": "Forbidden"}
        return render_to_response("explohyperfiction_error.html", data)
    if not Player.objects.filter(person=person):
        data={"message": "You are not member of ExploHyperfiction"}
        return render_to_response("explohyperfiction_error.html", data)
    player=Player.objects.get(person=person)
    if not player.is_manager:
        data={"message": "You must be manager"}
        return render_to_response("explohyperfiction_error.html", data)
    if not Event.objects.filter(id=int(id_event)):
        data={"message": "The event doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data)
    event=Event.objects.get(id=int(id_event))
    if player != event.manager:
        data={"message": "You are not manager of this event"}
        return render_to_response("explohyperfiction_error.html", data)
    data={"player":player, "login":True, "number_of_notices":len(SystemMessage.objects.filter(to=player)), "number_of_petitions":len(Petition.objects.all())}
    data["event"]=event
    challenges=Challenge.objects.filter(event=event, finish=False)
    data["challenges"]=Challenge.objects.filter(event=event, finish=False, phone=True)
    data["type"]=1
    latitude=0
    longitude=0
    num=0
    for challenge in challenges:
        latitude= latitude + challenge.user.person.position[1]
        longitude= longitude + challenge.user.person.position[0]
        num=num+1
    if len(challenges) !=0:
        data["longitude"]=longitude/num
        data["latitude"]=latitude/num
    template=get_template("explohyperfiction_monitor_event.html")
    return HttpResponse(template.render(RequestContext(request,data)))

def event_challenge(request,id_event,id_challenge):
    if not request.user.is_authenticated():
        data={"message": "You are not autheticated in LGS"}
        return render_to_response("explohyperfiction_error.html", data)
    if request.method !="GET":
        data={"message": "Forbidden"}
        return render_to_response("explohyperfiction_error.html", data)
    person=Person.objects.get(id=request.session["_auth_user_id"])
    if not Player.objects.filter(person=person):
        data={"message": "You are not member of ExploHyperfiction"}
        return render_to_response("explohyperfiction_error.html", data)
    player=Player.objects.get(person=person)
    if not Challenge.objects.filter(id=int(id_challenge)).exists():
        data={"message": "The challenge doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data)
    challenge=Challenge.objects.get(id=int(id_challenge))
    data={"player":player, "login":True, "number_of_notices":len(SystemMessage.objects.filter(to=player)), "number_of_petitions":len(Petition.objects.all())}
    data["event"]=challenge.event
    data["challenges"]=Challenge.objects.filter(event=challenge.event, finish=False)
    data["challenge_player"]=challenge
    data["longitude"]=challenge.user.person.position[0]
    data["latitude"]=challenge.user.person.position[1]
    data["type"]=0
    template=get_template("explohyperfiction_monitor_event.html")
    return HttpResponse(template.render(RequestContext(request,data)))


def json_position_player(request,id_player):
    player=Player.objects.get(id=id_player)
    data={"latitude":player.person.position[0],"longitude":player.person.position[1]}
    to_json={
        "latitude":player.person.position[0],
        "longitude":player.person.position[1]
    } 
    return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')
    
def json_position_event(request,id_event):
    event=Event.objects.get(id=id_event)
    challenges=Challenge.objects.filter(event=event, finish=False, phone=True)
    positionsJSON=[]
    for challenge in challenges:
        positionJSON={
            "name":challenge.user.person.username,
            "latitude":challenge.user.person.position[0],
            "longitude":challenge.user.person.position[1]
        } 
        positionsJSON.append(positionJSON)
    to_json={
        "positions":positionsJSON
    }
    return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')

def json_event_results(request,id_event):
    event=Event.objects.get(id=id_event)
    challenges=Challenge.objects.filter(event=event, finish=False, phone=True)
    responsesJSON=[]
    for challenge in challenges:
        response=Responses.objects.filter(challenge=challenge).order_by('-date')[0]
        responseJSON={
            "username":challenge.user.person.username,
            "question_id":str(response.question.id),
            "question_text":response.question.text,
            "answer_text":response.answer.text,
            "date":str(response.date),
            "next_question_id":str(response.answer.next),
            "next_question_text":Question.objects.get(id=response.answer.next).text
        }
        responsesJSON.append(responseJSON)
    to_json={
        "responses":responsesJSON
    }
    if len(challenges) == 0:
        to_json["exists"]=None

    return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')

def json_player_results(request, id_challenge, id_player):
    player=Player.objects.get(id=id_player)
    challenge=Challenge.objects.get(id=id_challenge)
    responsesJSON=[]
    responses=Responses.objects.filter(challenge=challenge).order_by('date')
    for response in responses:
        responseJSON={
            "question_id":str(response.question.id),
            "question_text":response.question.text,
            "answer_text":response.answer.text,
            "date":str(response.date)
        }
        responsesJSON.append(responseJSON)
    to_json={
        "username":challenge.user.person.username,
        "responses":responsesJSON,
    }
    if len(responses) == 0:
        to_json["exists"]=None

    return HttpResponse(simplejson.dumps(to_json), mimetype='application/json; charset="utf-8"')

