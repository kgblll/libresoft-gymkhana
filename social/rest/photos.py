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
from social.rest.forms import PhotoForm
from social.core.api_layer import get_data as layer_get_data
from social.layers.layers_manager import check_node_create
from social.layers.custom_exceptions.layers_manager_exceptions import *



from utils import error, get_limits, extract_params

PHOTO_FIELDS_BASIC = ["description", "latitude", "longitude"]
PHOTO_FIELDS_OPTIONAL = ["altitude", "avaliable_to", "avaliable_from"]
PHOTO_FIELDS_COMPLETE = PHOTO_FIELDS_BASIC + ["uploader", "photo_data", "photo_name"]

def photo_upload (request, layer_id):
	format = getResponseFormat (request)
	if not request.user.is_authenticated():
		return error (format, "The user is not authenticated")
	try:
		if request.method == "POST":
			
			success, params = extract_params (request.POST, PHOTO_FIELDS_BASIC, PHOTO_FIELDS_OPTIONAL)
			
			if not success:
				return error (format, "Need mandatory POST param: %s" % (params))
			
			try:
				check_node_create(layer_id)
			except Layer_Does_Not_Exist, err:
				return error(format, err)
			except Layer_Perms, err:
				return error(format, err)

			form = PhotoForm(request.POST, request.FILES)
			if form.is_valid():
				try:
					clean_data = form.cleaned_data
					params["photo_data"] = clean_data['photo']
					params["photo_name"] = clean_data['name']
					params["uploader"] = request.user.pk
					correct, message = api.photo.upload (params)
					if correct:
						photo_id = message
						correct, message = api.node.set_privacy_default(photo_id)
						if correct:
							correct, message = api.node.set_layer(photo_id, layer_id)
							if correct:
								data = {'code'		 : '200',
									'id'		   : photo_id,
									'description'  : 'Photo created correctly',}
								return generateResponse(format, data, "ok")
							else:
								error(format, message)
						else:
							error(format, message)
					else:
						return error(format, message)				
				except:
					return error (format, sys.exc_value)
			else:
				return error (format, "Sent data not valid")
		else:
			return error (format, "Need a POST petition")
	except Exception, err:
		return error (format, sys.exc_value)


"""
 Deprecated functionality:
"""


def photo_list (request):
	"""
	@deprecated: this function is deprecated above 1.0 version, search should be done
	using the layer api		
	"""
	format = getResponseFormat (request)
	if not request.user.is_authenticated():
		return error (format, "The user is not authenticated")
	try:
		f, t, page, elems = get_limits(request)
		photos = api.photo.get_all(f, t, request.user)
		#photos, page, elems = get_slice(request, photos)
		data = {'code'	: '200',
				'photos'  : photos,
				'page'	: page,
				'elems'   : len(photos),
				'type'	: "photo_list" }
		return generateResponse(format, data, "photo/list")
	except:
		return error(format, 'Some errors occurred')	

def photo_data(request, photo_id):
	"""
	@deprecated: this function is deprecated above 1.1 version, info should be requested
	using the layer api		
	"""	
	format = getResponseFormat (request)
	if not request.user.is_authenticated():
		return error (format, "The user is not authenticated")
	try:
		photo=api.photo.get_data(photo_id, request.user)
		if photo == None:
			return error(format, 'Photo doesn\'t exist')
		else:
			data = {"code"  : "200",
					"photo" : photo,
					"request" : request}
			return generateResponse(format, data, "photo/data")
	except:
		return error(format, "Some error occurred")
	


