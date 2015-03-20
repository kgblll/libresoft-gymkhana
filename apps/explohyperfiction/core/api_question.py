# -*- coding: UTF-8 -*-
from apps.explohyperfiction.models import *
import os

def create(request,event):
    if "qr" in request.POST.keys():
        qr=True
    else:
        qr=False
    if request.POST["before"]=="0":
        level=1
    else:
        ans=Answer.objects.get(id=int(request.POST["before"]))
        level=ans.question.level+1
    question= Question(event=event,
                       text=request.POST["text"],
                       qr=qr,
                       level=level)
    question.save()
    if request.POST["before"] != "0":
        ans=Answer.objects.get(id=int(request.POST["before"]))
        ans.next=question.id
        ans.save()
    
    if len(Question.objects.filter(event=event,qr=True))>0:
        event.qr=True
    else:
        event.qr=False
    event.save()
    
    if request.POST["text1"] != "":
            answer=Answer(question=question,
                  text=request.POST["text1"],
                  message=request.POST["message1"],)
            answer.save()
    if request.POST["text2"] != "":
            answer=Answer(question=question,
                  text=request.POST["text2"],
                  message=request.POST["message2"],)
            answer.save()
    if request.POST["text3"] != "":
            answer=Answer(question=question,
                  text=request.POST["text3"],
                  message=request.POST["message3"],)
            answer.save()
    if request.POST["text4"] != "":
            answer=Answer(question=question,
                  text=request.POST["text4"],
                  message=request.POST["message4"],)
            answer.save()
    if request.POST["text5"] != "":
            answer=Answer(question=question,
                  text=request.POST["text5"],
                  message=request.POST["message5"],)
            answer.save()
    return

def edit(request,question):
    if "qr" in request.POST.keys():
        qr=True
    else:
        qr=False
    question.text=request.POST["text"]
    question.qr=qr
    question.save()
    if len(Question.objects.filter(event=question.event,qr=True))>0:
        question.event.qr=True
    else:
        question.event.qr=False
    question.event.save()
    
    if request.POST["text1"] != "":
        if request.POST["answer1"] !="":
            answer=Answer.objects.get(id=int(request.POST["answer1"]))
            answer.text=text=request.POST["text1"]
            answer.message=request.POST["message1"]
            answer.save()
            if request.POST["next1"]!="0":
                answer.next=int(request.POST["next1"])
                answer.save()
        else:
            answer=Answer(question=question,
                  text=request.POST["text1"],
                  message=request.POST["message1"],)
            answer.save()
            if request.POST["next1"]!="0":
                answer.next=int(request.POST["next1"])
                answer.save()
    else:
        if request.POST["answer1"] !="":
            answer=Answer.objects.get(id=int(request.POST["answer1"]))
            answer.delete()
    if request.POST["text2"] != "":
        if request.POST["answer2"] !="":
            answer=Answer.objects.get(id=int(request.POST["answer2"]))
            answer.text=text=request.POST["text2"]
            answer.message=request.POST["message2"]
            answer.save()
            if request.POST["next2"]!="0":
                answer.next=int(request.POST["next2"])
                answer.save()
        else:
            answer=Answer(question=question,
                  text=request.POST["text2"],
                  message=request.POST["message2"],)
            answer.save()
            if request.POST["next2"]!="0":
                answer.next=int(request.POST["next2"])
                answer.save()
    else:
        if request.POST["answer2"] !="":
            answer=Answer.objects.get(id=int(request.POST["answer2"]))
            answer.delete()
    
    if request.POST["text3"] != "":
        if request.POST["answer3"] !="":
            answer=Answer.objects.get(id=int(request.POST["answer3"]))
            answer.text=text=request.POST["text3"]
            answer.message=request.POST["message3"]
            answer.save()
            if request.POST["next3"]!="0":
                answer.next=int(request.POST["next3"])
                answer.save()
        else:
            answer=Answer(question=question,
                  text=request.POST["text3"],
                  message=request.POST["message3"],)
            answer.save()
            if request.POST["next3"]!="0":
                answer.next=int(request.POST["next3"])
                answer.save()
    else:
        if request.POST["answer3"] !="":
            answer=Answer.objects.get(id=int(request.POST["answer3"]))
            answer.delete()
    
    if request.POST["text4"] != "":
        if request.POST["answer4"] !="":
            answer=Answer.objects.get(id=int(request.POST["answer4"]))
            answer.text=text=request.POST["text4"]
            answer.message=request.POST["message4"]
            answer.save()
            if request.POST["next4"]!="0":
                answer.next=int(request.POST["next4"])
                answer.save()
        else:
            answer=Answer(question=question,
                  text=request.POST["text4"],
                  message=request.POST["message4"],)
            answer.save()
            if request.POST["next4"]!="0":
                answer.next=int(request.POST["next4"])
                answer.save()
    else:
        if request.POST["answer4"] !="":
            answer=Answer.objects.get(id=int(request.POST["answer4"]))
            answer.delete()
    
    if request.POST["text5"] != "":
        if request.POST["answer5"] !="":
            answer=Answer.objects.get(id=int(request.POST["answer5"]))
            answer.text=text=request.POST["text5"]
            answer.message=request.POST["message5"]
            answer.save()
            if request.POST["next5"]!="0":
                answer.next=int(request.POST["next5"])
                answer.save()
        else:
            answer=Answer(question=question,
                  text=request.POST["text5"],
                  message=request.POST["message5"],)
            answer.save()
            if request.POST["next5"]!="0":
                answer.next=int(request.POST["next5"])
                answer.save()
    else:
        if request.POST["answer5"] !="":
            answer=Answer.objects.get(id=int(request.POST["answer5"]))
            answer.delete()
    
    return   

def delete(question):
    event=question.event
    answers=Answer.objects.filter(question=question)
    for answer in answers:
        os.remove(answer.image)
    question.delete()
    if len(Question.objects.filter(event=event,qr=True))>0:
        event.qr=True
    else:
        event.qr=False
    event.save()