# -*- coding: UTF-8 -*-
from apps.explohyperfiction.models import *
from datetime import datetime

def create(event,player,api):
    challenge=Challenge(event=event,
                        user=player,
                        finish=False,
                        phone=api,
                        date=datetime.now(),
                        cancel=False)
    challenge.save()
    return challenge