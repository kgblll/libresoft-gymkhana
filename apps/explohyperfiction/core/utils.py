# -*- coding: UTF-8 -*-

from apps.explohyperfiction.models import *
from apps.explohyperfiction.core import api
from cStringIO import StringIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.graphics.shapes import Image, Drawing
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.platypus.flowables import  ParagraphAndImage
from reportlab.lib.styles import getSampleStyleSheet
import qrcode
import os
from apps.explohyperfiction.urls import BASEDIR
import time


def print_question_pdf(question):
    answers=Answer.objects.filter(question=question)
    for answer in answers:
        img=qrcode.make(answer.text) 
        img.save(BASEDIR+"/img/"+str(answer.id)+".jpeg")
    response=HttpResponse(mimetype='application/pdf')
    response["Content-Disposition"]='attachment; filename= question_'+str(question.id)+".pdf"
    buffer=StringIO()
    style=getSampleStyleSheet()
    doc=SimpleDocTemplate(buffer)
    story=[Paragraph(question.text, style['Title'])]
    for answer in answers:
        story.append(Paragraph(question.event.name + "- ID:" + str(question.id)  , style['Title']))
        story.append(Image(BASEDIR+"/img/"+str(answer.id)+".jpeg", 100, 100))
        story.append(Paragraph(answer.text, style['Heading4']))
    doc.build(story)
    response.write(buffer.getvalue())
    for answer in answers:
        os.remove(BASEDIR+"/img/"+str(answer.id)+".jpeg")
    return response

def print_event_pdf(event):
    questions=Question.objects.filter(event=event, qr=True)
    for question in questions:
            answers=Answer.objects.filter(question=question)
            for answer in answers:
                img=qrcode.make(answer.text) 
                img.save(BASEDIR+"/img/"+str(answer.id)+".jpeg")
    response=HttpResponse(mimetype='application/pdf')
    response["Content-Disposition"]='attachment; filename= event_'+str(event.id)+".pdf"
    buffer=StringIO()
    style=getSampleStyleSheet()
    doc=SimpleDocTemplate(buffer)
    story=[Paragraph(event.name, style['Title'])]
    for question in questions:
            answers=Answer.objects.filter(question=question)
            story.append(Paragraph(question.text, style['Title']))
            for answer in answers:
                story.append(Paragraph(question.event.name + "- ID:" + str(question.id)  , style['Title']))
                story.append(Image(BASEDIR+"/img/"+str(answer.id)+".jpeg", 100, 100))
                story.append(Paragraph(answer.text, style['Heading4'])) 
    doc.build(story)
    response.write(buffer.getvalue())
    for question in questions:
            answers=Answer.objects.filter(question=question)
            for answer in answers:
                os.remove(BASEDIR+"/img/"+str(answer.id)+".jpeg") 
    return response
             
def get_max_level(event):
    questions=Question.objects.filter(event=event)
    max=0
    for q in questions:
        if max < q.level:
            max=q.level
    return max+1

def get_width(event):
    questions=Question.objects.filter(event=event)
    answers=Answer.objects.filter(question__event=event)
    max_questions=0
    max_level=get_max_level(event)
    for i in range(max_level):
        if len(Question.objects.filter(event=event, level=i))>max_questions:
            max_questions=len(Question.objects.filter(event=event, level=i))
    print max_questions
    width=max_questions*200 + len(answers)*11
    return width

def get_height(event):
    max_level=get_max_level(event)
    number=len(Answer.objects.filter(question__event=event))
    height=(max_level-1)*80 + 80 + (number)*7*(max_level-1)
    return height
 
def get_diff(event):
    questions=Question.objects.filter(event=event)
    return len(questions)*5  
