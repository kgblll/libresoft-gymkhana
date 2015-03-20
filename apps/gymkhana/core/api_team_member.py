#
#  Copyright (C) 2009 GSyC/LibreSoft
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>._
# 
#    Author : Jorge Fernandez Gonzalez <jorge.fernandez.gonzalez __at__ gmail.com>
#

import random

from social.core import api as api_lgs
from apps.gymkhana.models import *

def has_team(event, team_member):
    try:
      team_member_1 = team.teammember_set.get(event=event, user=team_member.user)
      return True, "ok", team_member_1
    except:
      return False, "Team Member Has Not Team.", None

#def create(team, first_name, last_name):
#    team_member = TeamMember()
#
#    num_team_members = len(team.teammember_set.all())
#    username = str(random.randint(0,1000)) + "-" + team.group.name
#    password = str(random.randint(0,1000)) + "-" + team.group.name
#    user = {'username': username, 'password': password, 'first_name': first_name, 'last_name': last_name}
#    correct, message = api_lgs.user.create_or_modify(user, modify=False)
#    if correct:
#      # message almacena user.id cuando todo ha ido correctamente
#      user = Person.objects.get(id=message)
#      team_member.user = user
#    else:
#      #return False, render_to_response('error.' + format, {'code': 500, 'description': message}) 
#      return False, message
#
#    team_member.team = team
#    team_member.save()
#    return True, "ok"

def create_by_user_id(event, team, user_id):
    #team = Team.objects.get(id=team_id)
    user = Person.objects.get(id=user_id)
    team_member = TeamMember(event=event, team=team, user=user)
    team_member.save()
    return True, "ok"

def join(event, team_id, session_user_id):
    user = Person.objects.get(id=session_user_id)
    team = Team(id=team_id)
    try:
      if type(TeamMember.objects.get(user=user,team=team)) == TeamMember:
        pass
        #return False, "Don't Repeat a Team Member."
    except:
      team_member = TeamMember(user=user,team=team)
      team_member.save()
    #first_proof = FirstProof.objects.get(event=event,team=team)
    return True, "ok"

def delete(team_member):
    # Esto borraria al usuario de la red social LGS, pero solo quiero eliminar al miembro del equipo.
    ## => Me corrijo a mi mismo: de momento solo dejo crear nuevos team_member que no pertenezcan ya a LGS,
    ## asi que cuando borre un team_member, lo borro todo.
    #team_member.user.delete()
    team_member.delete()
    return True, "ok"

#def list_previous_teams(team_member):

