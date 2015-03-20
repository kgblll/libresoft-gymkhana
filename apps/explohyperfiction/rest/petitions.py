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

def view_petitions(request):
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
    if not player.is_superuser:
        data={"message": "Only a superuser can see the resource"}
        return render_to_response("explohyperfiction_error.html", data)
    data={"login":True, "player":player, "number_of_petitions":len(Petition.objects.all()), "petitions":Petition.objects.all().order_by('-date')}
    template=get_template("explohyperfiction_petitions.html")
    return HttpResponse(template.render(RequestContext(request,data)))

def accept(request, id_petition):
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
    if not player.is_superuser:
        data={"message": "Only a superuser can see the resource"}
        return render_to_response("explohyperfiction_error.html", data)
    if not Petition.objects.filter(id=int(id_petition)).exists():
        data={"message": "The petition doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data)
    petition=Petition.objects.get(id=int(id_petition))
    if petition.for_manager:
        petition.player.is_manager=True
        group=Group.objects.get(name="Free Group")
        group.manager.add(petition.player)
        group.save()
    if petition.for_super:
        petition.player.is_superuser=True
    api.system_message.create_from_petition(petition, True)
    petition.player.save()
    petition.delete()
    return HttpResponseRedirect("/explohyperfiction/petitions/")

def reject(request, id_petition):
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
    if not player.is_superuser:
        data={"message": "Only a superuser can see the resource"}
        return render_to_response("explohyperfiction_error.html", data)
    if not Petition.objects.filter(id=int(id_petition)).exists():
        data={"message": "The petition doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data)
    petition=Petition.objects.get(id=int(id_petition))
    api.system_message.create_from_petition(petition, False)
    petition.delete()
    return HttpResponseRedirect("/explohyperfiction/petitions/")
