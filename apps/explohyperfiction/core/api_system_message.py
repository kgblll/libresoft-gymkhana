# -*- coding: UTF-8 -*-
from apps.explohyperfiction.models import *
from datetime import datetime

def create_from_petition(petition, accept):
    if accept:
        if petition.for_manager:
            message="Superuser has aceepted your request for manager"
        else:
            message="Superuser has accepted your request for superuser"
    else:
        if petition.for_manager:
            message="Superuser has rejected your request for manager"
        else:
            message="Superuser has rejected your request for superuser"
            
    system_message=SystemMessage(message=message, date=datetime.now())
    system_message.save()
    system_message.to.add(petition.player)
    system_message.save()
    
def create_manager(player, add):
    if add:
        message="Superuser makes you manager"
    else:
        message="Superuser quits your manager view"
    system_message=SystemMessage(message=message,date=datetime.now())
    system_message.save()
    system_message.to.add(player)
    system_message.save()
    
def join_group(petition,accept):
    if accept:
        message="You have been accepted in group " + str(petition.group.name)+"."
    else:
        message="You have been rejected in group " + str(petition.group.name)+"."
    system_message=SystemMessage(message=message,date=datetime.now())
    system_message.save()
    system_message.to.add(petition.player)
    system_message.save() 
    
def create_for_group_delete(player,group):
    system_message=SystemMessage(message="You have been deleted from the group " + str(group.name),date=datetime.now())
    system_message.save()
    system_message.to.add(player)
    system_message.save()
    
def create_for_manager(player,group):
    system_message=SystemMessage(message="You are manager of group" + str(group.name),date=datetime.now())
    system_message.save()
    system_message.to.add(player)
    system_message.save()