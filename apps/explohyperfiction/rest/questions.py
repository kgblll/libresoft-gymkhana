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


def create(request, id_event):
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
        template=get_template("explohyperfiction_manager_create_question.html")
        data={"player":player, "login":True, "number_of_notices":len(SystemMessage.objects.filter(to=player)), "number_of_petitions":len(Petition.objects.all())}
        data["event"]=event
        data["questions"]=Question.objects.filter(event=event)
        data["answers"]=Answer.objects.filter(question__event=event)
        return HttpResponse(template.render(RequestContext(request,data)))
    elif request.method=="POST":
        api.question.create(request,event)
        return HttpResponseRedirect("/explohyperfiction/events/manager/" + str(event.id)+"/questions/")
    else:
        data={"message": "Forbidden"}
        return render_to_response("explohyperfiction_error.html", data)
  
def edit(request, id_question):
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
    if not Question.objects.filter(id=int(id_question)):
        data={"message": "The question doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data)
    question=Question.objects.get(id=int(id_question))
    if player != question.event.manager:
        data={"message": "You are not manager of this event"}
        return render_to_response("explohyperfiction_error.html", data)
    if request.method=="GET":
        template=get_template("explohyperfiction_manager_create_question.html")
        data={"player":player, "login":True, "number_of_notices":len(SystemMessage.objects.filter(to=player)), "number_of_petitions":len(Petition.objects.all())}
        data["question"]=question
        data["questions"]=Question.objects.filter(event=question.event)
        data["answers"]=Answer.objects.filter(question__event=question.event)
        data["edit"]=True
        i=1
        for answer in Answer.objects.filter(question=question):
           data["answer"+str(i)]=answer
           i=i+1 
        return HttpResponse(template.render(RequestContext(request,data)))
    elif request.method=="POST":
        api.question.edit(request,question)
        return HttpResponseRedirect("/explohyperfiction/events/manager/" + str(question.event.id)+"/questions/")
    else:
        data={"message": "Forbidden"}
        return render_to_response("explohyperfiction_error.html", data) 
    
def view(request, id_question):
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
    data={"player":player, "login":True, "number_of_notices":len(SystemMessage.objects.filter(to=player)), "number_of_petitions":len(Petition.objects.all())}
    data["question"]=question
    data["answers"]=Answer.objects.filter(question=question)
    template=get_template("explohyperfiction_question_profile.html")
    return HttpResponse(template.render(RequestContext(request,data)))


def delete(request, id_question):
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
    id_event=question.event.id
    if Answer.objects.filter(next=question.id):
        answer=Answer.objects.get(next=question.id)
        answer.next=None
        answer.save()
    question.delete()
    return HttpResponseRedirect("/explohyperfiction/events/manager/" + str(id_event)+"/questions/")
   
def view_questions(request,id_event):
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
    template=get_template("explohyperfiction_list_questions.html")
    data={"player":player, "login":True, "number_of_notices":len(SystemMessage.objects.filter(to=player)), "number_of_petitions":len(Petition.objects.all())}
    data["event"]=event
    data["questions"]=Question.objects.filter(event=event)
    data["answers"]=Answer.objects.filter(question__event=event)
    return HttpResponse(template.render(RequestContext(request,data)))
