# -*- coding: UTF-8 -*-
from apps.explohyperfiction.models import *
from datetime import datetime

def response(petition,action):
    if action:
        petition.player.groups.add(petition.group)
        petition.player.save()
        newNotify=SystemMessage(to=petition.player,
                                message= "You have been accepted in group" + str(petition.group.name),
                                date=datetime.now())
        newNotify.save()
        petition.delete()
        return
    newNotify=SystemMessage(message= "You have been rejected in group" + str(petition.group.name),
                            date=datetime.now())
    newNotify.save()
    newNotify.to.add(petition.player)
    newNotify.save()
    petition.delete()
    return
    
def create(player,group):
    print group.name
    petition = PetitionGroup(player=player,
                             group=group,
                             date=datetime.now())
    petition.save()
    newNotify=SystemMessage(message= "You have a new request in group" + str(group.name),
                                date=datetime.now())
    newNotify.save()
    for manager in group.manager.all():
        newNotify.to.add(manager)
        newNotify.save()
    return