#
#  Copyright (C) 2011 GSyC/LibreSoft
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

from apps.gymkhana.models import *

def create(learning_objective):
    new_learning_objective = LearningObjective()
    new_learning_objective.objective = learning_objective
    new_learning_objective.save()

    return True, new_learning_objective

def list_all(event):
    #return True, LearningObjective.objects.get(event = event)
    return True, event.objectives.all()
