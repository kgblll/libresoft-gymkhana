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

def manager_create(request):
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
        template=get_template("explohyperfiction_manager_create_group.html")
        data={"player":player, "login":True, "number_of_notices":len(SystemMessage.objects.filter(to=player)), "number_of_petitions":len(Petition.objects.all())}
        return HttpResponse(template.render(RequestContext(request,data)))
    elif request.method=="POST":
        correct, group = api.group.create(request,player)
        if correct:
            return HttpResponseRedirect("/explohyperfiction/groups/manager/profile/" + str(group.id)+"/")
        else:
            data={}
            data["player"]=election_user
            data["group_exists"]=True
            template=get_template("groups_create.html")
            return HttpResponse(template.render(RequestContext(request,data)))
    else:
        data={"message": "Forbidden"}
        return render_to_response("explohyperfiction_error.html", data)
    
def manager_profile_group(request,id_group):
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
    if not Group.objects.filter(id=int(id_group)):
        data={"message": "The group doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data)
    group=Group.objects.get(id=int(id_group))
    if not player in group.manager.all():
        data={"message": "You are not manager of this group"}
        return render_to_response("explohyperfiction_error.html", data)
    data={"group":group,"player":player, "login":True, "number_of_notices":len(SystemMessage.objects.filter(to=player)), "number_of_petitions":len(Petition.objects.all())}
    data["players"]=Player.objects.filter(groups=group)
    data["managers"]=group.manager.all()    
    template=get_template("explohyperfiction_manager_profile_group.html")
    return HttpResponse(template.render(RequestContext(request,data)))

def manager_groups_view(request):
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
    groups=Group.objects.filter(manager=player)
    data={"groups":groups,"player":player, "login":True, "number_of_notices":len(SystemMessage.objects.filter(to=player)), "number_of_petitions":len(Petition.objects.all())}
    template=get_template("explohyperfiction_manager_view_groups.html")
    return HttpResponse(template.render(RequestContext(request,data)))

def manager_delete_group(request, id_group):
    if not request.user.is_authenticated():
        data={"message": "You are not autheticated in LGS"}
        return render_to_response("explohyperfiction_error.html", data)
    person=Person.objects.get(id=request.session["_auth_user_id"])
    if not Player.objects.filter(person=person):
        data={"message": "You are not member of ExploHyperfiction"}
        return render_to_response("explohyperfiction_error.html", data)
    if request.method !="GET":
        data={"message": "Forbidden"}
        return render_to_response("explohyperfiction_error.html", data)
    player=Player.objects.get(person=person)
    if not player.is_manager:
        data={"message": "You must be manager"}
        return render_to_response("explohyperfiction_error.html", data)
    if not Group.objects.filter(id=int(id_group)):
        data={"message": "The group doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data)
    group=Group.objects.get(id=int(id_group))
    if not player in group.manager.all():
        data={"message": "You are not manager of this group"}
        return render_to_response("explohyperfiction_error.html", data)
    if group.name=="Free Group":
        data={"message": "You can't delete the Free Group"}
        return render_to_response("explohyperfiction_error.html", data)
    group.delete()
    return HttpResponseRedirect("/explohyperfiction/groups/manager/view")

def manager_admin_members(request, id_group):
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
    if not Group.objects.filter(id=int(id_group)):
        data={"message": "The group doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data)
    group=Group.objects.get(id=int(id_group))
    if not player in group.manager.all():
        data={"message": "You are not manager of this group"}
        return render_to_response("explohyperfiction_error.html", data)
    if request.method !="GET":
        data={"message": "Forbidden"}
        return render_to_response("explohyperfiction_error.html", data)
    if group.name=="Free Group":
        data={"message": "You can't delete the Free Group"}
        return render_to_response("explohyperfiction_error.html", data)
    data={"group":group,"player":player, "login":True, "number_of_notices":len(SystemMessage.objects.filter(to=player)), "number_of_petitions":len(Petition.objects.all())}
    data["players"]=Player.objects.filter(group=group)
    data["managers"]=group.manager.all()
    template=get_template("explohyperfiction_manager_group_members.html")
    return HttpResponse(template.render(RequestContext(request,data)))
    
def manager_petitions(request, id_group):
    if not request.user.is_authenticated():
        data={"message": "You are not autheticated in LGS"}
        return render_to_response("explohyperfiction_error.html", data)
    person=Person.objects.get(id=request.session["_auth_user_id"])
    if not Player.objects.filter(person=person):
        data={"message": "You are not member of ExploHyperfiction"}
        return render_to_response("explohyperfiction_error.html", data)
    if request.method !="GET":
        data={"message": "Forbidden"}
        return render_to_response("explohyperfiction_error.html", data)
    player=Player.objects.get(person=person)
    if not player.is_manager:
        data={"message": "You must be manager"}
        return render_to_response("explohyperfiction_error.html", data)
    if not Group.objects.filter(id=int(id_group)):
        data={"message": "The group doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data)
    group=Group.objects.get(id=int(id_group))
    if not player in group.manager.all():
        data={"message": "You are not manager of this group"}
        return render_to_response("explohyperfiction_error.html", data)
    if not group.private:
        data={"message": "This is a free group"}
        return render_to_response("explohyperfiction_error.html", data)
    data={"player":player, "login":True, "number_of_notices":len(SystemMessage.objects.filter(to=player)), "number_of_petitions":len(Petition.objects.all())}
    data["petitions"]=PetitionGroup.objects.filter(group=group)
    template=get_template("explohyperfiction_manager_group_petitions.html")
    return HttpResponse(template.render(RequestContext(request,data)))

def manager_petition_accept(request,id_petition):
    if not request.user.is_authenticated():
        data={"message": "You are not autheticated in LGS"}
        return render_to_response("explohyperfiction_error.html", data)
    person=Person.objects.get(id=request.session["_auth_user_id"])
    if not Player.objects.filter(person=person):
        data={"message": "You are not member of ExploHyperfiction"}
        return render_to_response("explohyperfiction_error.html", data)
    if request.method !="GET":
        data={"message": "Forbidden"}
        return render_to_response("explohyperfiction_error.html", data)
    player=Player.objects.get(person=person)
    if not player.is_manager:
        data={"message": "You must be manager"}
        return render_to_response("explohyperfiction_error.html", data)
    if not PetitionGroup.objects.filter(id=int(id_petition)):
        data={"message": "The group petition doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data) 
    petition=PetitionGroup.objects.get(id=int(id_petition))
    if not player in petition.group.manager.all():
        data={"message": "You are not manager of this group"}
        return render_to_response("explohyperfiction_error.html", data)
    if not petition.group.private:
        data={"message": "This is a free group"}
        return render_to_response("explohyperfiction_error.html", data)
    url="/explohyperfiction/groups/manager/petitions/"+str(petition.group.id)+"/"
    api.petition_group.response(petition,True)
    return HttpResponseRedirect(url)

def manager_petition_reject(request,id_petition):
    if not request.user.is_authenticated():
        data={"message": "You are not autheticated in LGS"}
        return render_to_response("explohyperfiction_error.html", data)
    person=Person.objects.get(id=request.session["_auth_user_id"])
    if not Player.objects.filter(person=person):
        data={"message": "You are not member of ExploHyperfiction"}
        return render_to_response("explohyperfiction_error.html", data)
    if request.method !="GET":
        data={"message": "Forbidden"}
        return render_to_response("explohyperfiction_error.html", data)
    player=Player.objects.get(person=person)
    if not player.is_manager:
        data={"message": "You must be manager"}
        return render_to_response("explohyperfiction_error.html", data)
    if not PetitionGroup.objects.filter(id=int(id_petition)):
        data={"message": "The group petition doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data) 
    petition=PetitionGroup.objects.get(id=int(id_petition))
    if not player in petition.group.manager.all():
        data={"message": "You are not manager of this group"}
        return render_to_response("explohyperfiction_error.html", data)
    if not petition.group.private:
        data={"message": "This is a free group"}
        return render_to_response("explohyperfiction_error.html", data)
    url="/explohyperfiction/groups/manager/petitions/"+str(petition.group.id)+"/"
    api.petition_group.response(petition,False)
    return HttpResponseRedirect(url)
    
def user_group_profile(request,id_group):
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
    if not Group.objects.filter(id=int(id_group)):
        data={"message": "The group doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data)
    group=Group.objects.get(id=int(id_group))
    data={"group":group,"player":player, "login":True, "number_of_notices":len(SystemMessage.objects.filter(to=player)), "number_of_petitions":len(Petition.objects.all())}
    data["players"]=Player.objects.filter(groups=group)
    data["managers"]=group.manager.all()
    template=get_template("explohyperfiction_group_profile.html")
    return HttpResponse(template.render(RequestContext(request,data)))

def user_join(request,id_group):
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
    if not Group.objects.filter(id=int(id_group)):
        data={"message": "The group doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data)
    group=Group.objects.get(id=int(id_group))
    if group.private:
        data={"message": "This group requires auth"}
        return render_to_response("explohyperfiction_error.html", data)
    player.groups.add(group)
    player.save()
    return HttpResponseRedirect("/explohyperfiction/groups/user/view/")

def user_petition(request,id_group):
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
    if not Group.objects.filter(id=int(id_group)):
        data={"message": "The group doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data)
    group=Group.objects.get(id=int(id_group))
    if not group.private:
        return HttpResponseRedirect("explohyperfiction/user/join/"+str(id_group)+"/")
    if PetitionGroup.objects.filter(player=player, group=group).exists():
        data={"message": "The petition already exists"}
        return render_to_response("explohyperfiction_error.html", data)
    api.petition_group.create(player,Group.objects.get(id=int(id_group)))
    return HttpResponseRedirect("/explohyperfiction/groups/user/all/")

def user_petition_quit(request,id_group):
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
    if not Group.objects.filter(id=int(id_group)):
        data={"message": "The group doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data)
    group=Group.objects.get(id=int(id_group))
    if not group.private:
        return HttpResponseRedirect("explohyperfiction/user/join/"+str(id_group)+"/")
    if not PetitionGroup.objects.filter(player=player, group=group).exists():
        data={"message": "The petition doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data)
    petition=PetitionGroup.objects.get(player=player, group=group)
    petition.delete()
    return HttpResponseRedirect("/explohyperfiction/groups/user/all/")
    
    
def user_delete(request,id_group):
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
    if not Group.objects.filter(id=int(id_group)):
        data={"message": "The group doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data)
    group=Group.objects.get(id=int(id_group))
    if player in group.manager.all():
        data={"message": "You are manager of this group"}
        return render_to_response("explohyperfiction_error.html", data)
    player.groups.remove(group)
    player.save()
    return HttpResponseRedirect("/explohyperfiction/groups/user/view/")
    
def user_view(request):
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
    groups=player.groups.all()
    data={"groups":groups,"player":player, "login":True, "number_of_notices":len(SystemMessage.objects.filter(to=player)), "number_of_petitions":len(Petition.objects.all())}
    template=get_template("explohyperfiction_list_groups.html")
    data["petitions"]=PetitionGroup.objects.filter(player=player)
    return HttpResponse(template.render(RequestContext(request,data)))

def user_all(request):
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
    groups=Group.objects.all()
    data={"all":True,"groups":groups,"player":player, "login":True, "number_of_notices":len(SystemMessage.objects.filter(to=player)), "number_of_petitions":len(Petition.objects.all())}
    template=get_template("explohyperfiction_list_groups.html")
    data["petitions"]=PetitionGroup.objects.filter(player=player)
    data["my_groups"]=player.groups.all()
    data["petitions"]=PetitionGroup.objects.filter(player=player)
    return HttpResponse(template.render(RequestContext(request,data)))