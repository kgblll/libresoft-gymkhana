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


def enroll(request):
    if not request.user.is_authenticated():
        data={"message": "You are not autheticated in LGS"}
        return render_to_response("explohyperfiction_error.html", data)
    if request.method !="GET":
        data={"message": "Forbidden"}
        return render_to_response("explohyperfiction_error.html", data)
    api.player.new_player(request)
    return HttpResponseRedirect("/explohyperfiction/home/")

def register(request):
    if request.user.is_authenticated():
        data={"message": "You can't register if your logged"}
        return render_to_response("explohyperfiction_error.html", data)
    if request.method=="GET":
        template=get_template("explohyperfiction_user_register.html")
        return HttpResponse(template.render(RequestContext(request,{})))
    elif request.method=="POST":
        person = {'username':request.POST["username"].lower(),
                'password':request.POST["password"],
                'first_name':request.POST["first_name"],
                'last_name':request.POST["last_name"]}
        correct, message = api_lgs.user.create_or_modify(person, modify=False)
        if correct:
            data={"confirm":True}
            return render_to_response("explohyperfiction_user_register.html", data)
        else:
            data={"user_exists":True}
            template=get_template("explohyperfiction_user_register.html")
            return HttpResponse(template.render(RequestContext(request,data)))
    else:
        data={"message": "Forbidden"}
        return render_to_response("explohyperfiction_error.html", data)
    
def unenroll(request):
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
    player.delete()
    return HttpResponseRedirect("/explohyperfiction/home/")

def user_logout(request):
    if not request.user.is_authenticated():
        data={"message": "You are not autheticated in LGS"}
        return render_to_response("explohyperfiction_error.html", data)
    if request.method !="GET":
        data={"message": "Forbidden"}
        return render_to_response("explohyperfiction_error.html", data)
    logout(request)
    return HttpResponseRedirect("/explohyperfiction/home/")

def user_login(request):
    if request.user.is_authenticated():
        data={"message": "You are aleardy logged"}
        return render_to_response("explohyperfiction_error.html", data)
    if request.method=="GET":
        template=get_template("explohyperfiction_user_login.html")
        return HttpResponse(template.render(RequestContext(request,{})))
    elif request.method=="POST":
        loginform = LoginForm(request.POST)
        if loginform.login(request):
            return HttpResponseRedirect("/explohyperfiction/home/")
        else:
            template=get_template("explohyperfiction_user_login.html")
            data={"alert":True}
            return HttpResponse(template.render(RequestContext(request,data)))
    else:
        data={"message": "Forbidden"}
        return render_to_response("explohyperfiction_error.html", data)
        
def superuser(request):
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
    player.is_superuser=True
    player.is_manager=True
    player.save()
    group=Group.objects.get(name="Free Group")
    group.manager.add(player)
    group.save()
    return HttpResponseRedirect("/explohyperfiction/home/")

def select_view(request):
    if not request.user.is_authenticated():
        data={"message": "You are not autheticated in LGS"}
        return render_to_response("explohyperfiction_error.html", data)
    if request.method !="POST":
        data={"message": "Forbidden"}
        return render_to_response("explohyperfiction_error.html", data)
    person=Person.objects.get(id=request.session["_auth_user_id"])
    if not Player.objects.filter(person=person):
        data={"message": "You are not member of ExploHyperfiction"}
        return render_to_response("explohyperfiction_error.html", data)
    player=Player.objects.get(person=person)
    if request.POST["view"]=="superuser":
        if player.is_superuser:
            player.active_superuser=True
            player.active_manager=False
            player.active_player=False
            player.save()
        else:
            data={"message": "You can't see the superuser view because you are not superuser"}
            return render_to_response("explohyperfiction_error.html", data)
    if request.POST["view"]=="manager":
        if player.is_manager:
            player.active_superuser=False
            player.active_manager=True
            player.active_player=False
            player.save()
        else:
            data={"message": "You can't see the manager view because you are not manager"}
            return render_to_response("explohyperfiction_error.html", data)
    if request.POST["view"]=="player":
        if player.is_player:
            player.active_superuser=False
            player.active_manager=False
            player.active_player=True
            player.save()
        else:
            data={"message": "You can't see the player view because you are not player"}
            return render_to_response("explohyperfiction_error.html", data)
    return HttpResponseRedirect("/explohyperfiction/home/")