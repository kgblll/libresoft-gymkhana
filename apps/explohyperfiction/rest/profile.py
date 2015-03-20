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

def view_profile(request):
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
    data={"player":player, "login":True, "number_of_notices":len(SystemMessage.objects.filter(to=player)), "number_of_petitions":len(Petition.objects.all()),"petition_superuser":api.petition.exists_petition_for_superuser(player), "petition_manager":api.petition.exists_petition_for_manager(player)}
    template=get_template("explohyperfiction_user_profile.html")
    return HttpResponse(template.render(RequestContext(request,data)))

def petitions(request, mode):
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
    if mode =="superuser":
        if api.petition.exists_petition_for_superuser(player):
            data={"message": "The petition already exists"}
            return render_to_response("explohyperfiction_error.html", data)
        api.petition.create_for_superuser(player)
    if mode =="manager":
        if api.petition.exists_petition_for_manager(player):
            data={"message": "The petition already exists"}
            return render_to_response("explohyperfiction_error.html", data)
        api.petition.create_for_manager(player)
    return HttpResponseRedirect("/explohyperfiction/profile/")

def petitions_delete(request, mode):
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
    if mode =="superuser":
        if not api.petition.exists_petition_for_superuser(player):
            data={"message": "The petition doesn't exists"}
            return render_to_response("explohyperfiction_error.html", data)
        api.petition.delete_for_superuser(player)
    if mode =="manager":
        print mode
        if not api.petition.exists_petition_for_manager(player):
            data={"message": "The petition doesn't exists"}
            return render_to_response("explohyperfiction_error.html", data)
        api.petition.delete_for_manager(player)
    return HttpResponseRedirect("/explohyperfiction/profile/")

def quit(request, mode):
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
    if mode =="superuser":
        player.is_superuser=False
        player.save()
    if mode =="manager":
        player.is_manager=False
        player.save()
        group=Group.objects.get(name="Free Group")
        group.manager.remove(player)
        group.save()
    return HttpResponseRedirect("/explohyperfiction/profile/")