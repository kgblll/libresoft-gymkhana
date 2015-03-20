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

from utils import error

def node_tag(request, node_id):
	format = getResponseFormat (request)
	if not request.user.is_authenticated():
		return error(format, "The user is not authenticated")
	if request.method == "POST":
		if "tags" in request.POST:
			tags=request.POST["tags"]
			correct, message = api.node.set_tag(node_id, tags)
			if correct:
				data = { 'code'		 : '200',
						 'description'  : 'Tags set correctly'}
				return generateResponse(format, data, "ok")
			else:
				return error(format, message) 
		else:
			return error (format, 'Missing parameters')
	else:
		return error (format, 'Need a POST petition')
	
def node_untag(request, node_id):
	format = getResponseFormat (request)
	if not request.user.is_authenticated():
		return error(format, "The user is not authenticated")
	if request.method == "POST":
		if "tags" in request.POST:
			tags=request.POST["tags"]
			correct, message = api.node.remove_tag(node_id, tags)
			if correct:
				data = { 'code'		 : '200',
						 'description'  : 'Tags removed correctly'}
				return generateResponse(format, data, "ok")
			else:
				return error(format, message) 
		else:
			return error (format, 'Missing parameters')
	else:
		return error (format, 'Need a POST petition')	

def node_comment(request, node_id):
	format = getResponseFormat (request)
	if not request.user.is_authenticated():
		return error(format, "The user is not authenticated")
	if request.method == "POST":
		if "comment" in request.POST:
			comment=request.POST["comment"]
			correct, message = api.node.set_comment(node_id, comment, request.user.id)
			if correct:
				data = { 'code'		 : '200',
						 'description'  : 'Comment added correctly'}
				return generateResponse(format, data, "ok")
			else:
				return error(format, message) 
		else:
			return error (format, 'Missing parameters')
	else:
		return error (format, 'Need a POST petition')
	
def node_delete_comment(request):
	format = getResponseFormat (request)
	if not request.user.is_authenticated():
		return error(format, "The user is not authenticated")
	if request.method == "POST":
		if "comment_id" in request.POST:
			comment_id = request.POST["comment_id"]
			correct, message = api.node.delete_comment(comment_id, request.user.id)
			if correct:
				data = { 'code'		 : '200',
						 'description'  : 'Comment deleted correctly'}
				return generateResponse(format, data, "ok")
			else:
				return error(format, message) 
		else:
			return error (format, 'Missing parameters')
	else:
		return error (format, 'Need a POST petition')



def node_set_position (request, node_id):
	format = getResponseFormat (request)
	if not request.user.is_authenticated():
		return error(format, "The user is not authenticated")
	if request.method == "POST":
		if ("latitude" in request.POST) and ("longitude" in request.POST):
			latitude=request.POST["latitude"]
			longitude=request.POST["longitude"]
			if ("radius" in request.POST):
				radius=request.POST["radius"]
			else:
				radius=None
			if ("altitude" in request.POST):
				altitude=request.POST["altitude"]
			else:
				altitude=None
			if radius != None and altitude != None:
				correct, message = api.node.set_coordinates(node_id, latitude, longitude, altitude=altitude, radius=radius)
			elif radius != None:
				correct, message = api.node.set_coordinates(node_id, latitude, longitude, radius=radius)
			elif altitude != None:
				correct, message = api.node.set_coordinates(node_id, latitude, longitude, altitude=altitude)
			else:
				correct, message = api.node.set_coordinates(node_id, latitude, longitude)
			if correct:
				data = { 'code'		 : '200',
						 'description'  : 'Position updated'}
				return generateResponse(format, data, "ok")
			else:
				return error(format, message)
		else:
			return error (format, 'Missing parameters')
	else:
		return error (format, 'Need a POST petition')
	
	
"""
 Deprecated functionality:
"""

def node_list(request):
	"""
	@deprecated: this function is deprecated above 1.1 version, info should be requested
	using the layer api		
	"""	
	format = getResponseFormat (request)
	if not request.user.is_authenticated():
		return error(format, "The user is not authenticated")
	nodes=api.node.get_all(request.user)
	data = {"code"  : '200',
			"nodes" : nodes }
	return generateResponse(format, data, "nodes/list")

def node_data(request, node_id):
	"""
	@deprecated: this function is deprecated above 1.1 version, info should be requested
	using the layer api		
	"""	
	format = getResponseFormat (request)
	if not request.user.is_authenticated():
		return error (format, "The user is not authenticated")
	try:
		node=api.node.get_data(node_id, request.user)
		if node == None:
			return error(format, 'Node doesn\'t exist')
		else:
			data = {"code" : "200",
					"node" : node}
			return generateResponse(format, data, "nodes/data")
	except:
		return error(format, 'Some errors occurred')


def node_near(request, node):
	format = getResponseFormat (request)
	if not request.user.is_authenticated():
		return error(format, "The user is not authenticated")
	try:
		radius=request.REQUEST["r"]
	except:
		return error(format, 'Need a (get or post) "r" parameter with the radius')
	nodes=api.node.get_nearby_node(node, radius, request.user)
	data = {"code"  : '200',
			"nodes" : nodes }
	return generateResponse(format, data, "nodes/dist")
