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

import sys

from format.utils import  getResponseFormat, generateResponse
from social.core import api
from social.core.api_layer import get_data as layer_get_data
from social.rest.forms import SoundForm
from social.layers.layers_manager import check_node_create
from social.layers.custom_exceptions.layers_manager_exceptions import *

from django.http import HttpResponse

from utils import error, get_limits, extract_params

SOUND_FIELDS_BASIC = ["description", "latitude", "longitude"]
SOUND_FIELDS_OPTIONAL = ["altitude", "avaliable_to", "avaliable_from"]
SOUND_FIELDS_COMPLETE = SOUND_FIELDS_BASIC + ["owner", "sound_data", "sound_name"]

def sound_upload (request, layer_id):
	format = getResponseFormat (request)
	if not request.user.is_authenticated():
		return error (format, "The user is not authenticated")
	try:
		if request.method == "POST":
			
			success, params = extract_params (request.POST, SOUND_FIELDS_BASIC, SOUND_FIELDS_OPTIONAL)
			
			if not success:
				return error (format, "Need mandatory POST param: %s" % (params))
			
			try:
				check_node_create(layer_id)
			except Layer_Does_Not_Exist, err:
				return error(format, err)
			except Layer_Perms, err:
				return error(format, err)
			
			params["owner"] = request.user.id
			form = SoundForm(request.POST, request.FILES)
			if form.is_valid():
				try:
					clean_data = form.cleaned_data
					params["sound_data"] = clean_data['sound']
					params["sound_name"] = clean_data['name']
					params["uploader"] = request.user.pk
					correct, message = api.sound.upload (params)
					
					if correct:
						sound_id = message
						correct, message = api.node.set_privacy_default(sound_id)
						if correct:
							correct, message = api.node.set_layer(sound_id, layer_id)
							if correct:
								data = {'code'		 : '200',
									'id'		   : sound_id,
									'description'  : 'Sound created correctly',}
								return generateResponse(format, data, "ok")
							else:
								return error(format, message)
						else:
							return error(format, message) 
					else:
						return error(format, message)
				except:
					return error (format, sys.exc_value)
			else:
				return error (format, "Sent data not valid")
		else:
			return error (format, "Need a POST petition")
	except:
		return error (format, sys.exc_info())


"""
 Deprecated functionality:
"""

def sound_list (request):
	"""
	@deprecated: this function is deprecated above 1.0 version, search should be done
	using the layer api		
	"""
	format = getResponseFormat (request)
	if not request.user.is_authenticated():
		return error (format, "The user is not authenticated")
	try:
		f, t, page, elems = get_limits(request)
		sounds = api.sound.get_all(f, t, request.user)
		#sounds, page, elems = get_slice(request, sounds)
		data = {'code'	: '200',
				'sounds'  : sounds,
				'page'	: page,
				'elems'   : len(sounds),
				'type'	: "photo_list" }
		return generateResponse(format, data, "sound/list")
	except:
		return error(format, 'Some errors occurred') 

def sound_data(request, sound_id):
	"""
	@deprecated: this function is deprecated above 1.1 version, info should be requested
	using the layer api		
	"""
	format = getResponseFormat (request)
	if not request.user.is_authenticated():
		return error (format, "The user is not authenticated")
	try:
		sound=api.sound.get_data(sound_id, request.user)
		if sound == None:
			return error(format, 'Sound doesn\'t exist')
		else:
			data = {"code"  : "200",
					"sound" : sound,
					"request" : request}
			return generateResponse(format, data, "sound/data")
	except:
		return error(format, "Some error occurred")

def sound_file(request, sound_id):
	"""
	@deprecated: this function is deprecated above 1.1 version, info should be requested
	using the layer api		
	"""
	format = getResponseFormat (request)
	if not request.user.is_authenticated():
		return error (format, "The user is not authenticated")
	try:
		file_path=api.sound.get_file_path(sound_id, viewer=request.user) 
		if file_path == None:
			return error(format, 'Sound doesn\'t exist or you don\'t have permission for view it')
		file_data = open(file_path, "rb").read()
		return HttpResponse(file_data, mimetype="audio/3gpp")
	except:
		return error(format, "Some error occurred")


