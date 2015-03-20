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

# This file defines the api that must be used instead of accessing 
#  directly to the data models.

import privacy
import api_user as user
import api_group as group
import api_node as node
import api_note as note
import api_photo as photo
import api_sound as sound
import api_video as video

from django.contrib.contenttypes.models import ContentType

from utils import get_person
from social.core.config import ALLOWED_SEARCH


def get_version():
    return "1.2.1" 
    
def tags(models, tag, viewer):
    """
    Returns a list
    """
    results={}
    try:
        v=get_person(viewer)
    except:
        return []
    for model in models:
        if model in ALLOWED_SEARCH:
            tagged=[]
            try:
                model_type = ContentType.objects.get(name=model, app_label="core").model_class() 
                for t in model_type.objects.filter(tags__tag=tag):
                    tagged+=[t.get_dictionary(v)]
            except:
                pass
            results[model]=tagged
    return results

