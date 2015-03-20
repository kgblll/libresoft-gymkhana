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


# Create your views here.

from format.utils import  getResponseFormat, generateResponse
from social.core import api
from social.core.config import ALLOWED_SEARCH
from social.layers import layers_manager
from django.http import HttpResponse

from social.layers.custom_exceptions.layers_manager_exceptions import *
from social.core.custom_exceptions.social_core_exceptions import *

from utils import error, get_limits, get_num_pages, get_slice, get_authenticated_user
import string

def version(request):
	format = getResponseFormat (request)
	ver=api.get_version()
	data={"code"   : "200",
		  "version": ver}
	return generateResponse(format, data, "version")

def forbbiden_photo(request):
	format = getResponseFormat (request)	
	return error(format, "You don't have permission to access here", code='405')

	
def search(request):
	"""
	@deprecated: this function is deprecated above 1.0 version, search should be done
	using the layer api		
	"""
	
	format = getResponseFormat(request)
	if not request.user.is_authenticated():
		return error (format, "The user is not authenticated")
	
	if "dist" in request.REQUEST:
		dist=request.REQUEST["dist"]
	else:
		dist=-1
	if "terms" in request.REQUEST:
		terms=request.REQUEST["terms"]
	else:
		terms=""
	if "models" in request.REQUEST:
		models = string.split(request.REQUEST["models"])
	else:
		models = ALLOWED_SEARCH
	results=api.search (request.user, models, terms, dist)
	data ={"code"   : "200",
		   "results": results}
	
	return generateResponse(format, data, "search/list")

def tag_list(request, tag):
	"""
	@deprecated: this function is deprecated above 1.0 version, search should be done
	using the layer api		
	"""
	format = getResponseFormat(request)
	if not request.user.is_authenticated():
		return error (format, "The user is not authenticated")
	
	if "models" in request.REQUEST:
		models = string.split(request.REQUEST["models"])
	else:
		models = ALLOWED_SEARCH
	results=api.tags(models, tag, request.user.id)
	data ={"code"   : "200",
		   "results": results}
	
	return generateResponse(format, data, "search/list")

def node_delete(request, layer_id, node_id):
	
	format = getResponseFormat (request)
	if not request.user.is_authenticated():
		return error(format, "The user is not authenticated")
	
	try:
		result = layers_manager.check_node_delete(layer_id, node_id)
	
		if result:	
			result, message = api.node.delete(node_id, request.user.id)
			if result:
				data = {'code'		 : '200',
						'description'  : 'Node deleted correctly',}
				return generateResponse(format, data, "ok")
			else:
				return error(format, message)

		return error(format, "Error deleting node")
		
	except Layer_Does_Not_Exist, err:
		return error(format, err)
	except Layer_Perms, err:
		return error(format, err)
	except Layer_Node, err:
		return error(format, err)
	except:
		return error(format, "Error deleting the note")
	
def node_data(request, layer_id, node_id):
	format = getResponseFormat (request)
	
	user = get_authenticated_user (request.user, allow_anonymous = True)
	if user == None:
		return error(format, "The user is not authenticated and not anonymous allowed")
	
	try:
		
		node = layers_manager.get_node_data(layer_id, node_id, user)
		
		if node == None:
			return error(format, 'Node doesn\'t exist')
		else:
			data = {"code" : "200",
					"results" : [node]}
			return generateResponse(format, data, "node/list")	
			
	except Layer_Does_Not_Exist, err:
		return error(format, err)
	except Layer_Node, err:
		return error(format, err)
	except Exception, err:
		print err
	
		return error(format, 'Some errors occurred')


def node_image(request, layer_id, node_id, thumb=False, size=None):
	
	format = getResponseFormat (request)
	user = get_authenticated_user (request.user, allow_anonymous = True)
	if user == None:
		return error(format, "The user is not authenticated and not anonymous allowed")
	try:
		image = layers_manager.get_node_image(layer_id, node_id, user, size, thumb)

		if image == None:
			return error(format, 'Photo doesn\'t exist or you don\'t have permission for view it')

		return HttpResponse(image, mimetype="image/jpeg")
	
	except Social_Core_Exception, err:
		return error(format, err)
	except Layer_Does_Not_Exist, err:
		return error(format, err)
	except Layer_Node, err:
		return error(format, err)
	except Exception, err:
		print err
		
def node_sound_file(request, layer_id, node_id):
	
	format = getResponseFormat (request)
	user = get_authenticated_user (request.user, allow_anonymous = True)
	if user == None:
		return error(format, "The user is not authenticated and not anonymous allowed")
	try:
		
		sound = layers_manager.get_node_sound(layer_id, node_id, user)
		
		if sound == None:
			return error(format, 'Sound doesn\'t exist or you don\'t have permission for view it')

		return HttpResponse(sound, mimetype="audio/3gpp")
	except Social_Core_Exception, err:
		return error(format, err)
	except Layer_Does_Not_Exist, err:
		return error(format, err)
	except Layer_Node, err:
		return error(format, err)
	except Exception, err:
		print err

def node_video_file(request, layer_id, node_id):
	
	format = getResponseFormat (request)
	user = get_authenticated_user (request.user, allow_anonymous = True)
	if user == None:
		return error(format, "The user is not authenticated and not anonymous allowed")
	try:
		
		video = layers_manager.get_node_video(layer_id, node_id, user)
		
		if video == None:
			return error(format, 'Video doesn\'t exist or you don\'t have permission for view it')

		return HttpResponse(video, mimetype="video/3gpp")
	except Social_Core_Exception, err:
		return error(format, err)
	except Layer_Does_Not_Exist, err:
		return error(format, err)
	except Layer_Node, err:
		return error(format, err)
	except Exception, err:
		print err		
		
def node_set_dates(request, layer_id, node_id):
	
	format = getResponseFormat (request)
	if not request.user.is_authenticated():
		return error (format, "The user is not authenticated")
	try:
		avaliable_from = None
		avaliable_to = None
		
		if "avaliable_from" in request.REQUEST:
			avaliable_from = request.REQUEST["avaliable_from"]
		
			
		if "avaliable_to" in request.REQUEST:
			avaliable_to = request.REQUEST["avaliable_to"]
		
			
		if avaliable_to == None and avaliable_from == None:
			return error(format, "You have to specify at least on of these: avaliable_to or avaliable_from dates")
		 
		layers_manager.set_node_dates(layer_id, node_id, request.user, avaliable_from, avaliable_to)
		
		data = {'code'		 : '200',
				'description'  : 'Dates updated correctly',}
		
		return generateResponse(format, data, "ok")
			
	except Social_Date_Exceptions, err:
		return error(format, err)
	except Social_Core_Exception, err:
		return error(format, err)
	except Layer_Does_Not_Exist, err:
		return error(format, err)
	except Layer_Node, err:
		return error(format, err)
	except Exception, err:
		return error(format, err)
			
def node_get_layers(request, node_id):
	
	format = getResponseFormat (request)
	
	user = get_authenticated_user (request.user, allow_anonymous = True)
	if user == None:
		return error(format, "The user is not authenticated and not anonymous allowed")
	try:
		
		layers = layers_manager.get_node_layers(node_id, user)
		
		f, t, page, elems = get_limits(request)
		total_pages = get_num_pages(len(layers), elems)
		layers = get_slice(layers, f, t)

		data = {'code'		 : 200, 
				'page'   : page,
				'elems'   : len(layers),
				'total_pages' : total_pages,
				'results'  : layers}
		
		return generateResponse(format, data, "node/list" )
		
	except Social_Core_Exception, err:
		return error(format, err)
	except Layer_Does_Not_Exist, err:
		return error(format, err)
	except Layer_Node, err:
		return error(format, err)
	except Exception, err:
		print err
	