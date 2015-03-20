# -*- coding: UTF-8 -*-


from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from datetime import datetime

from django.contrib.auth import authenticate, login, logout

from social.core import api as api_lgs
from social.rest.forms import LoginForm
from social.core.models import *
from apps.explohyperfiction.core import utils
from apps.explohyperfiction.models import *
from apps.explohyperfiction.core import api

def view_events(request):
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
    if not player.active_player:
        data={"message": "You must be player"}
        return render_to_response("explohyperfiction_error.html", data)
    data={"player":player, "login":True, "number_of_notices":len(SystemMessage.objects.filter(to=player)), "number_of_petitions":len(Petition.objects.all())}
    data["events"]=Event.objects.filter(group__in=player.groups.all(),active=True).order_by("-date")
    template=get_template("explohyperfiction_list_events.html")
    return HttpResponse(template.render(RequestContext(request,data)))

def view_events_by_group(request):
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
    if not player.active_player:
        data={"message": "You must be player"}
        return render_to_response("explohyperfiction_error.html", data)
    data={"player":player, "login":True, "number_of_notices":len(SystemMessage.objects.filter(to=player)), "number_of_petitions":len(Petition.objects.all())}
    data["events_groups"]=True
    data["groups"]=player.groups.all()
    template=get_template("explohyperfiction_list_events.html")
    return HttpResponse(template.render(RequestContext(request,data)))

def view_events_of_group(request,id_group):
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
    if not player.active_player:
        data={"message": "You must be player"}
        return render_to_response("explohyperfiction_error.html", data)
    if not Group.objects.filter(id=int(id_group)):
        data={"message": "The group doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data)
    group=Group.objects.get(id=int(id_group))
    data={"player":player, "login":True, "number_of_notices":len(SystemMessage.objects.filter(to=player)), "number_of_petitions":len(Petition.objects.all())}
    data["events"]=Event.objects.filter(group=group,active=True).order_by("-date")
    template=get_template("explohyperfiction_list_events.html")
    return HttpResponse(template.render(RequestContext(request,data)))

def view_events_started(request):
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
    if not player.active_player:
        data={"message": "You must be player"}
        return render_to_response("explohyperfiction_error.html", data)
    data={"player":player, "login":True, "number_of_notices":len(SystemMessage.objects.filter(to=player)), "number_of_petitions":len(Petition.objects.all())}
    template=get_template("explohyperfiction_list_challenges.html")
    return HttpResponse(template.render(RequestContext(request,data)))
