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


def view_groups(request):
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
    data={"login":True, "player":player, "number_of_petitions":len(Petition.objects.all()), "groups":Group.objects.all().order_by('name'), "petitions":Petition.objects.all()}
    template=get_template("explohyperfiction_list_groups.html")
    return HttpResponse(template.render(RequestContext(request,data)))

def view_groups_profile(request,id_group):
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
    if not Group.objects.filter(id=int(id_group)):
        data={"message": "The group doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data)
    group=Group.objects.get(id=int(id_group))
    data={"group":group,"player":player, "login":True, "number_of_notices":len(SystemMessage.objects.filter(to=player)), "number_of_petitions":len(Petition.objects.all())}
    data["players"]=Player.objects.filter(groups=group)
    data["managers"]=group.manager.all()
    template=get_template("explohyperfiction_group_profile.html")
    return HttpResponse(template.render(RequestContext(request,data)))   
    
def view_groups_delete(request,id_group):
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
    if not Group.objects.filter(id=int(id_group)):
        data={"message": "The group doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data)
    group=Group.objects.get(id=int(id_group))
    if group.name =="Free Group":
        data={"message": "You cant delete the free group"}
        return render_to_response("explohyperfiction_error.html", data)
    group.delete()
    return HttpResponseRedirect("/explohyperfiction/admin/groups/")   

def view_users(request):
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
    data={"login":True, "player":player, "number_of_petitions":len(Petition.objects.all()), "players":Player.objects.all().order_by('person__username'), "petitions":Petition.objects.all()}
    template=get_template("explohyperfiction_list_users.html")
    return HttpResponse(template.render(RequestContext(request,data)))

def view_user_profile(request, id_player):
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
    if not Player.objects.filter(id=int(id_player)):
        data={"message": "The player doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data)
    data={"login":True, "player":player, "p":Player.objects.get(id=int(id_player)), "number_of_petitions":len(Petition.objects.all()), "players":Player.objects.all(), "petitions":Petition.objects.all()}
    template=get_template("explohyperfiction_admin_user_profile.html")
    return HttpResponse(template.render(RequestContext(request,data)))

def user_delete(request,id_player):
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
    if not Player.objects.filter(id=int(id_player)):
        data={"message": "The player doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data)
    p=Player.objects.get(id=int(id_player))
    if p.is_superuser:
        data={"message": "You can't admin a superuser"}
        return render_to_response("explohyperfiction_error.html", data)
    p.delete()
    return HttpResponseRedirect("/explohyperfiction/admin/users/")

def user_manager(request,id_player):
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
    if not Player.objects.filter(id=int(id_player)):
        data={"message": "The player doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data)
    p=Player.objects.get(id=int(id_player))
    if p.is_superuser:
        data={"message": "You can't admin a superuser"}
        return render_to_response("explohyperfiction_error.html", data)
    p.is_manager=True
    p.save()
    group=Group.objects.get(name="Free Group")
    group.manager.add(p)
    group.save()
    api.system_message.create_manager(p,True)
    if api.petition.exists_petition_for_manager(p):
        petition=api.petition.get_petition_for_manager(p)
        petition.delete()
    return HttpResponseRedirect("/explohyperfiction/admin/users/")

def user_manager_quit(request,id_player):
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
    if not Player.objects.filter(id=int(id_player)):
        data={"message": "The player doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data)
    p=Player.objects.get(id=int(id_player))
    if p.is_superuser:
        data={"message": "You can't admin a superuser"}
        return render_to_response("explohyperfiction_error.html", data)
    p.is_manager=False
    p.save()
    group=Group.objects.get(name="Free Group")
    group.manager.remove(p)
    group.save()
    api.system_message.create_manager(p,False)
    if api.petition.exists_petition_for_manager(p):
        petition=api.petition.get_petition_for_manager(p)
        petition.delete()
    return HttpResponseRedirect("/explohyperfiction/admin/users/")

    