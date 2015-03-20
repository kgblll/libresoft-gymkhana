#
#  Copyright (C) 2009 GSyC/LibreSoft
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU Affero General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU Affero General Public License for more details.
#
#	You should have received a copy of the GNU Affero General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
#	Author : Jose Antonio Santos Cadenas <jcaden __at__ gsyc __dot__ es>
#

from social.core.utils import get_person_by_name
from format.utils import generateResponse

from social.rest.custom_exceptions.rest_interface_exceptions import BAD_PAGES_REQUEST 

PAGE = 0
N_ELEMS = 15

def error (format, message, code='500'):
	data = {'code'		 : code,
			'description'  : message,}
	return generateResponse(format, data, "error")

def get_elements_per_page():
	return N_ELEMS

def get_num_pages(total_elems, elems_page):
	
	total_pages = total_elems / elems_page
	mod = total_elems % elems_page
	if mod != 0:
		total_pages = total_pages + 1
	
	return total_pages

def get_slice(nodes, from_limit, to_limit):
	
	return nodes[from_limit:to_limit]

def get_limits(request):
	if "page" in request.REQUEST:
		page = request.REQUEST["page"]
	else:
		page = None
	if "elems" in request.REQUEST:
		elems = request.REQUEST["elems"]
	else:
		elems = None
	try:
		page = int(page) - 1
		if page < 0:
			raise ValueError()
	except:
		page = PAGE
	try:
		elems = int(elems)
		if elems < 0:
			raise ValueError()
	except:
		elems=N_ELEMS
	f = elems * page
	t = f + elems
	return (f, t, page+1, elems)

def get_requested_page(request, nodes_list):
	
	from_elms, to_elms, page, elems = get_limits(request)

	if from_elms == 0 and to_elms == 0 and int(request.REQUEST["page"]) != 0:
		raise BAD_PAGES_REQUEST
	
	if from_elms == 0 and to_elms == 0:
		to_elms = len(nodes_list)
		total_pages = 1
	else:
		n_total_elems = len (nodes_list)
		total_pages = get_num_pages(n_total_elems, elems)
		
	node_list = get_slice(nodes_list, from_elms, to_elms)
	
	return node_list, page, total_pages

def _extract_params(request, fields, mandatory = False):
	
	fields_dict = {}

	for field in fields:
		if not field in request:
			if mandatory:
				return False, field
		else:
			fields_dict[field] = request[field]

	return True, fields_dict

def extract_params(request, mandatory_fields, optional_fields = None):
	params = {}
	params_opt = {}
	
	success, params = _extract_params (request, mandatory_fields, True)
	
	if not success:
		return False, params

	if optional_fields != None:
		success, params_opt = _extract_params (request, optional_fields, False)
		params.update(params_opt)
	
	return True, params

def get_authenticated_user(user, allow_anonymous = False):
	
	if not user.is_authenticated():
		if allow_anonymous:
			anonymous = get_person_by_name("anonymous")
			user = anonymous
		else:
			return None
	return user


def generateRESTResponse(request, social_nodes, user, format, backup = False):
	
	from social.export_manager.export_manager import Export_Manager
	from social.rest.custom_exceptions.rest_interface_exceptions import Bad_Request
	
	""" 
		stuff to support pages in the request
	"""
	try:
		node_list, page, total_pages = get_requested_page (request, social_nodes)
		page_dict = { "page" : page, 
					"total_pages": total_pages}
	except Bad_Request, msg:
		return error (format, msg) 
	
	exportManager = Export_Manager()		
	exportManager.configure(format.lower(), "HTTPResponse", backup = backup, viewer= user)
	
		
	return exportManager.export(node_list, page_dict, user)


