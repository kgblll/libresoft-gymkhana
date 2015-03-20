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

from models import Groupifier

import pickle

def update_groups():
    """
    Executes all the groupifiers looking for new groups
    """
    groupifiers= Groupifier.objects.all()
    for g in groupifiers:
        #if g.name=="geo":
            algorithm_class = pickle.loads(g.algorithm.encode("ascii"))
            name = g.name
            data_model = pickle.loads(g.data_set_model.encode("ascii"))
            data_query = pickle.loads(g.data_set_query.encode("ascii"))
            data = data_model.objects.all()
            data.query = data_query
            init_groups =  g.groups.all()
            extra_params = pickle.loads(g.extra_params.encode("ascii"))
            functions_class = pickle.loads(g.functions.encode("ascii"))
            functions = functions_class()
            min_members = g.min_members                     
            min_dist = g.min_dist
            a=algorithm_class(name=name, data=data, functions=functions,
                              initial_groups=init_groups, groupifier=g,
                              extra_params=extra_params, 
                              min_members=min_members, min_dist=min_dist,)
            a.run()