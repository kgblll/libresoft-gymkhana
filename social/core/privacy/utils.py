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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
#    Author : Jose Antonio Santos Cadenas <jcaden __at__ gsyc __dot__ es>
#


#In this module all the role defining functions will be implemented

from social.core.models import Group, Membership, Person, Friendship


def get_group_members(requested, viewer, params):
    group_id=params["group_id"]
    group = Group.objects.get(pk=group_id)
    user_ids=Membership.objects.get_relations_for(group)
    return Person.objects.filter(pk__in=user_ids)

def get_friends(requested, viewer, params):
    try:
        type = requested.type
        if "person" == type:
            user_ids=Friendship.objects.get_relations_for(requested)
            return Person.objects.filter(pk__in=user_ids)
        elif "note" == type:
            return get_friends(requested.uploader, viewer, params)
        elif "photo" == type:
            return get_friends(requested.uploader, viewer, params)
        else:
            return Person.objects.none()
    except:
        return Person.objects.none()

def get_friends_of_friends(requested, viewer, params):
    try:
        type = requested.type
        if "person" == type:
            user_ids=Friendship.objects.get_relations_for(requested)
            friends = Person.objects.filter(pk__in=user_ids)
            for friend in friends:
                user_ids +=Friendship.objects.get_relations_for(friend)
            user_ids=list(set(user_ids))
            user_ids.remove(requested.id)
            return Person.objects.filter(pk__in=user_ids)
        elif "note" == type:
            return get_friends_of_friends(requested.uploader, viewer, params)
        elif "photo" == type:
            return get_friends_of_friends(requested.uploader, viewer, params)
        else:
            return Person.objects.none()
    except:
        return Person.objects.none()

def get_all(requested, viewer, params):
    return Person.objects.all()

