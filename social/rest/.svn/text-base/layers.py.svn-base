# -*- coding: utf-8 -*-
#
#  Copyright (C) 2009-20010 Universidad Rey Juan Carlos, GSyC/LibreSoft
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
#	Author : Jose Gato Luis <jgato@libresoft.es>

from django.http import HttpResponse

from format.utils import  getResponseFormat, generateResponse
from social.layers.layers_manager import layers_info, layers_search, layers_icon, layers_categories, layers_list, layers_delete, layers_create, layers_change_icon, layer_is_external
from social.core.api_node import set_privacy_default
from social.layers.custom_exceptions.layers_manager_exceptions import *
from social.rest.custom_exceptions.rest_interface_exceptions import Bad_Request

from utils import error, get_authenticated_user, get_requested_page, generateRESTResponse

import sys
from social.rest.forms import IconForm
from social.core.config import MAX_ICON_UPLOAD_SIZE

LAYER_FIELDS_BASIC = ["name", "description", "latitude", "longitude"]
LAYER_FIELDS_COMPLETE = LAYER_FIELDS_BASIC + ["owner", "layer_type", "writeable", "free", "external"]



def create_layer(request):
	
	format = getResponseFormat (request)
	 
	if not request.user.is_authenticated():
		return error(format, "The user is not authenticated")
	try:	
		if request.method == "POST":
				layer = {}
				
				for field in LAYER_FIELDS_BASIC:
					if field in request.POST:
						layer[field] = request.POST[field]
						
				layer["owner"] = request.user.pk
				"""
					Currently, users can only create layers as:
						* user layer (non officials)
						* free 
						* internal
				"""
				layer["layer_type"] = "USR"
				layer["writeable"] = True
				layer["free"] = True
				layer["external"] = False
				
				success, response = layers_create(layer)
				
				if success:
					layer_id = response
					success, response = set_privacy_default(layer_id)
					if success:
						data = {'code'		 : '200',
								'id'		   : layer_id,
								'description'  : 'Layer created correctly',}
						return generateResponse(format, data, "ok")
				return error(format, response)
				
		else:
			return error(format, "Need a POST petition")
	except:
		return error (format, sys.exc_value)

def request_layer(request, layer_id = None, multi_search = False):
	
	format = getResponseFormat (request)
	 
	user = get_authenticated_user (request.user, allow_anonymous = True)
	if user == None:
		return error(format, "The user is not authenticated and not anonymous allowed")

	if "search" in request.GET:
		search = request.GET["search"]
	else:
		return error(format, "\"search\" parameter is mandatory")
	
	backup = False
	if "backup" in request.GET:
		if request.GET["backup"].lower() == "true":
			backup = True
		
	options = request.GET.copy()
	options["user"] = user
	
		
	if multi_search == True:
		options["category"] = "0"
		if "layers" not in options:
			return error(format, "Error in the request")
		layers = options["layers"].split(",")
		if backup:
			for layer in layers:
				if layer_is_external(layer, user):
					return error(format, "No export allowed of external layers in backup mode") 
				
	else:
		if layer_id == None:
			return error(format, "Error in the request")
		layers = layer_id
		if backup and layer_is_external(layer_id, user):
					return error(format, "No export allowed of external layers in backup mode")
	success, response = layers_search(layers, search, options, multi_search)
	
	
	if success:
		return generateRESTResponse(request, response, user, str(format), backup)
	else:
		return error(format, response)

def categories_layer(request, layer_id):
	
	format = getResponseFormat (request)
	 
	user = get_authenticated_user (request.user, allow_anonymous = True)
	if user == None:
		return error(format, "The user is not authenticated and not anonymous allowed")
	
	success, response = layers_categories(layer_id)
	
	if success:
		data = {'code'		 : "200",
				'results'  : response}
		
		return generateResponse(format, data, "category/list" )
	else:
		return error(format, response)
	
def info_layer(request, layer_id):

	format = getResponseFormat (request)
	
	user = get_authenticated_user (request.user, allow_anonymous = True)
	if user == None:
		return error(format, "The user is not authenticated and not anonymous allowed")
	
	success, response = layers_info(layer_id)
	
	if success:
		data = {'code'		 : 200,
				'description'  : response,}
		return generateResponse(format, data, "ok" )
	else:
		return error(format, response)




def list_layer(request):

	format = getResponseFormat (request)
	
	user = get_authenticated_user (request.user, allow_anonymous = True)
	if user == None:
		return error(format, "The user is not authenticated and not anonymous allowed")
		
	try:
		user_layer = False
		if "user_layer" in request.GET and request.GET["user_layer"].lower() == "true":
			user_layer = True

		success, response = layers_list(user, user_layer)
		
		if success:
			return generateRESTResponse(request, response, user, str(format))
		else:
			return error(format, response)
	except Exception, e:
		print e
		return error(format, "Error in layer list")

def icon_layer(request, layer_id):
	
	format = getResponseFormat (request)
	
	user = get_authenticated_user (request.user, allow_anonymous = True)
	if user == None:
		return error(format, "The user is not authenticated and not anonymous allowed")

	success, data = layers_icon(layer_id)
	
	if success:
		return HttpResponse(data, mimetype="image/png")
	else:
		return error(format, data)
	

def icon_change_layer(request, layer_id):
	
	format = getResponseFormat (request)
	
	user = get_authenticated_user (request.user, allow_anonymous = False)
	if user == None:
		return error(format, "The user is not authenticated and not anonymous allowed")


	form = IconForm(request.POST, request.FILES)
	if form.is_valid():
		try:
			
			
			
			params = {}
			clean_data = form.cleaned_data
			params["icon_data"] = clean_data['icon']
			params["icon_name"] = clean_data['name']
			params["uploader"] = request.user.pk
			
			if params["icon_data"].size / 1000 > MAX_ICON_UPLOAD_SIZE:
				return error(format, "icon max size " + str(MAX_ICON_UPLOAD_SIZE) + "kb") 
			
			success = layers_change_icon(layer_id, user, params)
			
			if success:
				data = {'code'		 : '200',
						'id'		   : layer_id,
						'description'  : 'Icon updated correctly',}
				return generateResponse(format, data, "ok")
			else:
				return error(format, "Error changing icon")
		except IOError, err:
			return error(format, err)
		except Layer_Does_Not_Exist, err:
			return error(format, err)
		except Layer_Perms, err:
			return error(format, err)
	else:
		return error (format, "Sent data not valid")


	
def delete_layer (request, layer_id):
	format = getResponseFormat (request)
	if not request.user.is_authenticated():
		return error(format, "The user is not authenticated")
	
	correct, message = layers_delete(layer_id, request.user.id)
	
	if correct:
		data = {'code'		 : '200',
				'description'  : 'Layer deleted correctly',}
		return generateResponse(format, data, "ok")
	else:
		return error(format, message)			   


	
