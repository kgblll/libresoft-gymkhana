# -*- coding: utf-8 -*-
#
#  Copyright (C) 2009-20010 Universidad Rey Juan Carlos, GSyC/LibreSoft
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
#	 Author : Jose Antonio Santos Cadenas <jcaden __at__ gsyc __dot__ es>
#    Author : Jose Gato Luis <jgato@libresoft.es>


from format.utils import  getResponseFormat, generateResponse
from social.core import api
from social.core.api_layer import  get_data as layer_get_data
from social.layers.layers_manager import check_node_create
from social.layers.custom_exceptions.layers_manager_exceptions import *

from utils import error, get_limits, extract_params

NOTE_FIELDS_BASIC = ["text", "title", "latitude", "longitude"]
NOTE_FIELDS_OPTIONAL = ["altitude", "avaliable_to", "avaliable_from"]
NOTE_FIELDS_COMPLETE = NOTE_FIELDS_BASIC + ["owner"]

def note_upload (request, layer_id):
	format = getResponseFormat (request)
	if not request.user.is_authenticated():
		return error(format, "The user is not authenticated")
	if request.method == "POST":
		if request.user.is_authenticated():
			
			success, params = extract_params (request.POST, NOTE_FIELDS_BASIC, NOTE_FIELDS_OPTIONAL)
			
			if not success:
				return error (format, "Need mandatory POST param: %s" % (params))
			
			try:
				check_node_create(layer_id)
			except Layer_Does_Not_Exist, err:
				return error(format, err)
			except Layer_Perms, err:
				return error(format, err)
			
			params["owner"] = request.user.id
			correct, message = api.note.create(params)
			
			if correct:
				note_id = message
				correct, message = api.node.set_privacy_default(note_id)
				if correct:
					correct, message = api.node.set_layer(note_id, layer_id)
					if correct:
						data = {'code'		 : '200',
							'id'		   : note_id,
							'description'  : 'Note created correctly',}
						return generateResponse(format, data, "ok")
					else:
						return error(format, message)
				else:
					return error(format, message)
			else:
				return error(format, message)				
		else:
			return error(format, "The user must be logged in")
	else:
		return error(format, 'Need a POST petition')

"""
 Deprecated functionality:
"""

def note_list (request):
	"""
	@deprecated: this function is deprecated above 1.0 version, search should be done
	using the layer api		
	"""
	format = getResponseFormat (request)
	if not request.user.is_authenticated():
		return error (format, "The user is not authenticated")
	try:
		f, t, page, elems = get_limits(request)
		notes = api.note.get_all(f, t, viewer=request.user)
		#notes, page, elems = get_slice(request, notes)
		data = {'code'	: '200',
				'notes'   : notes,
				'page'	: page,
				'elems'   : len(notes),
				'type'	: "note_list" }
		return generateResponse(format, data, "note/list")
	except:
		return error(format, 'Some errors occurred')
	


