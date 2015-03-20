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

from apps.gymkhana.models import *

def create(possible_solution, challenge):
    solution = Solution()
    solution.possible_solution = possible_solution
    solution.challenge = challenge
    solution.save()
    return True, solution

def list_all():
    return True, Solution.objects.all()
