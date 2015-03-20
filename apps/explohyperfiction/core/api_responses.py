# -*- coding: UTF-8 -*-
from apps.explohyperfiction.models import *
from django.contrib.gis.geos import Point
from datetime import datetime

def create(challenge,question,answer):
    response=Responses(challenge=challenge,
                       question=question,
                       date=datetime.now(),
                       answer=answer)
    response.save()