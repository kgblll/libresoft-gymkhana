# -*- coding: UTF-8 -*-
from apps.explohyperfiction.models import *
from datetime import datetime

def create_for_manager(player): #IN: ElectionUser
    petition = Petition(player=player,
                        for_super=False,
                        for_manager=True,
                        date= datetime.now())
    petition.save()
    return

def create_for_superuser(player): #IN: ElectionUser
    petition = Petition(player=player,
                        for_super=True,
                        for_manager=False,
                        date= datetime.now())
    petition.save()
    return

def exists_petition_for_manager(player): # IN: ElectionUser #OUT:Boolean
    if Petition.objects.filter(player=player, for_manager=True):
        return True
    return False


def exists_petition_for_superuser(player): # IN: ElectionUser #OUT:Boolean
    if Petition.objects.filter(player=player, for_super=True):
        return True
    return False
def delete_for_manager(player):
    petition=get_petition_for_manager(player)
    petition.delete()
    return
    
def delete_for_superuser(player):
    petition=get_petition_for_superuser(player)
    petition.delete()
    return
def get_petition_for_manager(player): # IN: ElectionUser; OUT: Petition
    return Petition.objects.get(player=player, for_manager=True)

def get_petition_for_superuser(player): # IN: ElectionUser; OUT: Petition
    return Petition.objects.get(player=player, for_super=True)