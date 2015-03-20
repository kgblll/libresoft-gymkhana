# -*- coding: UTF-8 -*-
from apps.explohyperfiction.models import *
def create_free_group():
    if not Group.objects.filter(name="Free Group").exists():
        group=Group(name="Free Group",
                    private=False,
                    description="Free group for everyone!")
        group.save()
    return


def create(request,player):
    if Group.objects.filter(name=request.POST["name"]).exists():
        return False, None
    if request.POST.has_key("private"):
        private=True
    else:
        private=False
        
    group= Group(name= request.POST["name"],
                     private=private,
                     description=request.POST["description"])
    group.save()
    group.manager.add(player)
    group.save()
    player.groups.add(group)
    group.save()
    return True,group

def edit(request,group):
    if not request.POST["name"]==group.name:
        if Group.objects.filter(name=request.POST["name"]).exists():
            return False
    if request.POST.has_key("private"):
        private=True
    else:
        private=False
        
    group.name=request.POST["name"]
    group.private=private
    group.description=request.POST["description"]
    group.save()
    return True    