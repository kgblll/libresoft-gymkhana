from apps.explohyperfiction.models import *
from datetime import datetime

def create(request,player):
    if Event.objects.filter(name=request.POST["name"]).exists():
        return False, None
    event=Event(name=request.POST["name"],
                description=request.POST["description"],
                manager=player,
                active=False,
                qr=False,
                date=datetime.now(),
                attemps=1)
    event.save()
    if "Free Group" in request.POST.keys():
        g=Group.objects.get(name="Free Group")
        event.group.add(g)
        event.save()
    for g in request.POST.keys():
        if Group.objects.filter(name=g, manager=player).exists():
            group=Group.objects.get(name=g)
            event.group.add(group)
            event.save()
    event.save()
    return True,event

def edit(request,event):
    if request.POST["name"] != event.name:
        if Event.objects.filter(name=request.POST["name"]).exists():
            return False,event
        
    event.name=request.POST["name"]
    event.description=request.POST["description"]
    event.save()
    for g in request.POST.keys():
        if Group.objects.filter(name=g, manager=event.manager).exists():
            group=Group.objects.get(name=g)
            if not group in event.group.all():
                event.group.add(group)
                event.save()
    for g in event.group.all():
        if not g.name in request.POST.keys():
            event.group.remove(g)
            event.save()
    return True,event