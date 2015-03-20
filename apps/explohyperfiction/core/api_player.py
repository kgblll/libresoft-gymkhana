# -*- coding: UTF-8 -*-
from apps.explohyperfiction.models import *
def new_player(request):
    person=Person.objects.get(id=request.session["_auth_user_id"])
    if not Player.objects.filter(person=person).exists():
        player=Player(person=person,
                      is_superuser=False,
                      is_manager=False,
                      is_player=True,
                      active_superuser=False,
                      active_manager=False,
                      active_player=True)
        player.save()
        player.groups.add(Group.objects.get(name="Free Group"))
        player.save()
    return 