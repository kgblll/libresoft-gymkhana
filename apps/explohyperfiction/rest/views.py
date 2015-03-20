# -*- coding: UTF-8 -*-

from apps.explohyperfiction.rest import user
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.shortcuts import render_to_response

from apps.explohyperfiction.core import api
from apps.explohyperfiction.core import utils
from apps.explohyperfiction.models import *

from social.core import api as api_lgs
from social.rest.forms import LoginForm
from social.core.models import *

def home(request):
    data={}
    api.group.create_free_group()
    if request.user.is_authenticated():
        data["login"]=True
        data["name"]=request.user.username
        person=Person.objects.get(id=request.session["_auth_user_id"])
        if Player.objects.filter(person=person).exists():
            data["member"]=True
            player=Player.objects.get(person=person)
            data["player"]=player
            data["number_of_notices"]=len(SystemMessage.objects.filter(to=player))
    if(len(Player.objects.filter(is_superuser=True))<1):
        data["superuser"]=True
    if request.method!="GET":
        data["message"]="Forbidden operation"
        return render_to_response("explohyperfiction_error.html", data)
    data["number_of_petitions"]=len(Petition.objects.all())
    template=get_template("explohyperfiction_base.html")
    return HttpResponse(template.render(RequestContext(request,data)))

def print_question(request,id_question):
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
    if not Question.objects.filter(id=int(id_question)):
        data={"message": "The question doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data)
    question=Question.objects.get(id=int(id_question))
    if player != question.event.manager:
        data={"message": "You are not manager of this event"}
        return render_to_response("explohyperfiction_error.html", data)
    return utils.print_question_pdf(question)

def print_event(request,id_event):
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
    return utils.print_event_pdf(event) 
