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

def create(request):
    if not request.user.is_authenticated():
        data={"message": "You are not autheticated in LGS"}
        return render_to_response("explohyperfiction_error.html", data)
    person=Person.objects.get(id=request.session["_auth_user_id"])
    if not Player.objects.filter(person=person):
        data={"message": "You are not member of ExploHyperfiction"}
        return render_to_response("explohyperfiction_error.html", data)
    player=Player.objects.get(person=person)
    if not player.is_manager:
        data={"message": "You must be manager"}
        return render_to_response("explohyperfiction_error.html", data)
    if request.method=="GET":
        template=get_template("explohyperfiction_manager_create_event.html")
        data={"player":player, "login":True, "number_of_notices":len(SystemMessage.objects.filter(to=player)), "number_of_petitions":len(Petition.objects.all())}
        data["groups"]=Group.objects.filter(manager=player)
        return HttpResponse(template.render(RequestContext(request,data)))
    elif request.method=="POST":
        correct, event = api.event.create(request,player)
        if correct:
            return HttpResponseRedirect("/explohyperfiction/events/manager/profile/" + str(event.id)+"/")
        else:
            data={"player":player, "login":True, "number_of_notices":len(SystemMessage.objects.filter(to=player)), "number_of_petitions":len(Petition.objects.all())}
            data["groups"]=Group.objects.filter(manager=player)
            data["group_exists"]=True
            template=get_template("explohyperfiction_manager_create_event.html")
            return HttpResponse(template.render(RequestContext(request,data)))
    else:
        data={"message": "Forbidden"}
        return render_to_response("explohyperfiction_error.html", data)


def edit(request, id_event):
    if not request.user.is_authenticated():
        data={"message": "You are not autheticated in LGS"}
        return render_to_response("explohyperfiction_error.html", data)
    person=Person.objects.get(id=request.session["_auth_user_id"])
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
    if request.method=="GET":
        template=get_template("explohyperfiction_manager_create_event.html")
        data={"edit":True,"player":player, "login":True, "number_of_notices":len(SystemMessage.objects.filter(to=player)), "number_of_petitions":len(Petition.objects.all())}
        data["groups"]=Group.objects.filter(manager=player)
        data["event"]=event
        data["groups_event"]=event.group.all()
        return HttpResponse(template.render(RequestContext(request,data)))
    elif request.method=="POST":
        correct, event = api.event.edit(request,event)
        if correct:
            return HttpResponseRedirect("/explohyperfiction/events/manager/profile/" + str(event.id)+"/")
        else:
            data={"edit":True, "player":player, "login":True, "number_of_notices":len(SystemMessage.objects.filter(to=player)), "number_of_petitions":len(Petition.objects.all())}
            data["groups"]=Group.objects.filter(manager=player)
            data["group_exists"]=True
            data["event"]=event
            data["groups_event"]=event.group.all()
            template=get_template("explohyperfiction_manager_create_event.html")
            return HttpResponse(template.render(RequestContext(request,data)))
    else:
        data={"message": "Forbidden"}
        return render_to_response("explohyperfiction_error.html", data)
    
def profile(request,id_event):
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
    data["groups"]=event.group.all()
    data["event"]=event
    template=get_template("explohyperfiction_manager_profile_event.html")
    return HttpResponse(template.render(RequestContext(request,data)))

def active(request,id_event):
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
    event.active=True
    event.save()
    return HttpResponseRedirect("/explohyperfiction/events/manager/profile/" + str(event.id)+"/")

def active(request,id_event):
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
    if event.active:
        event.active=False
    else:
        event.active=True
    event.date=datetime.now()
    event.save()
    return HttpResponseRedirect("/explohyperfiction/events/manager/profile/" + str(event.id)+"/")

def view(request):
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
    if not player.is_manager:
        data={"message": "You must be manager"}
        return render_to_response("explohyperfiction_error.html", data)
    data={"player":player, "login":True, "number_of_notices":len(SystemMessage.objects.filter(to=player)), "number_of_petitions":len(Petition.objects.all())}
    data["events"]=Event.objects.filter(manager=player)
    template=get_template("explohyperfiction_list_events.html")
    return HttpResponse(template.render(RequestContext(request,data)))

def delete(request, id_event):
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
    event.delete()
    return HttpResponseRedirect("/explohyperfiction/events/manager/view/")


def view_map(request,id_event):
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
    data={}
    data["questions"]=Question.objects.filter(event=event)
    data["answers"]=Answer.objects.filter(question__event=event)
    data["width"]=utils.get_width(event)
    data["height"]=utils.get_height(event)
    data["max_level"]=utils.get_max_level(event)
    data["y_diff"]=utils.get_diff(event)
    template=get_template("explohyperfiction_map.html")
    return HttpResponse(template.render(Context(data)))


