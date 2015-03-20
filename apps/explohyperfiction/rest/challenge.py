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

def start(request, id_event):
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
    if not Event.objects.filter(id=int(id_event)):
        data={"message": "The event doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data)
    event=Event.objects.get(id=int(id_event))
    challenge=api.challenge.create(event,player,False)
    question=Question.objects.filter(event=event,level=1)[0]
    return HttpResponseRedirect("/explohyperfiction/challenges/"+str(challenge.id)+"/question/"+str(question.id)+"/")

def question(request, id_challenge, id_question):
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
    if not Challenge.objects.filter(id=int(id_challenge), user=player).exists():
        data={"message": "The challenge doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data)
    if not Question.objects.filter(id=int(id_question)).exists():
        data={"message": "The Question doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data)
    challenge=Challenge.objects.get(id=int(id_challenge))
    question=Question.objects.get(id=int(id_question))
    if (question.event != challenge.event):
        data={"message": "This question is from other event"}
        return render_to_response("explohyperfiction_error.html", data)
    data={"player":player, "login":True, "number_of_notices":len(SystemMessage.objects.filter(to=player)), "number_of_petitions":len(Petition.objects.all())}
    data["question"]=question
    data["answers"]=Answer.objects.filter(question=question)
    data["challenge"]=challenge
    template=get_template("explohyperfiction_player_question.html")
    return HttpResponse(template.render(RequestContext(request,data)))  

def answer(request, id_challenge, id_question, id_answer):
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
    if not Challenge.objects.filter(id=int(id_challenge), user=player).exists():
        data={"message": "The challenge doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data)
    if not Question.objects.filter(id=int(id_question)).exists():
        data={"message": "The Question doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data)
    if not Answer.objects.filter(id=int(id_answer)).exists():
        data={"message": "The answer doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data)
    challenge=Challenge.objects.get(id=int(id_challenge))
    question=Question.objects.get(id=int(id_question))
    answer=Answer.objects.get(id=int(id_answer))
    if (question.event != challenge.event) or (answer.question != question ):
        data={"message": "This question is not of this challenge"}
        return render_to_response("explohyperfiction_error.html", data)
    api.responses.create(challenge,question,answer)
    if answer.next != None:
        return HttpResponseRedirect("/explohyperfiction/challenges/"+str(challenge.id)+"/question/"+str(answer.next)+"/")
    else:
        return HttpResponseRedirect("/explohyperfiction/challenges/"+str(challenge.id)+"/finish/")
    
def finish(request,id_challenge):
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
    if not Challenge.objects.filter(id=int(id_challenge), user=player).exists():
        data={"message": "The challenge doesn't exists"}
        return render_to_response("explohyperfiction_error.html", data)
    challenge=Challenge.objects.get(id=int(id_challenge))
    challenge.date_finish=datetime.now()
    challenge.finish=True
    challenge.save()
    return HttpResponseRedirect("/explohyperfiction/results/player/"+str(challenge.id)+"/")

