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

def group_create (request):
	format = getResponseFormat (request)
	if not request.user.is_authenticated():
		return error(format, "The user is not authenticated")
	if request.method == "POST":
		if ("groupname" in request.POST):
			group={'groupname':request.POST["groupname"]}
			correct, message=api.group.create_or_modify(group, modify=False)
			if correct:
				data = {'code'		 : '200',
						'id'		   : message,
						'description'  : 'Group created correctly',}
				return generateResponse(format, data, "ok")
			else:
				return error(format, message)			   
		else:
			return error(format, 'Missing parameters')
	else:
		return error(format, 'Need a POST petition')

def group_list (request):
	format = getResponseFormat (request)
	if not request.user.is_authenticated():
		return error(format, "The user is not authenticated")
	try:
		groups=api.group.get_all(request.user.id)
		data = {'code'	  : '200',
				'groups'   : groups}
		return generateResponse(format, data, "group/list")
	except:
		return error(format, 'Some errors occurred')

def group_data (request, group):
	format = getResponseFormat (request)
	if not request.user.is_authenticated():
		return error(format, "The user is not authenticated")
	try:
		group=api.group.get_data(group, request.user.id)
		if group == None:
			return error(format, 'Group doesn\'t exist')
		else:
			data = {"code" : "200",
					"group" : group,
					"request" : request}
			return generateResponse(format, data, "group/data")
	except:
		return error(format, 'Group doesn\'t exist')

def group_elements(request, group):
	format = getResponseFormat (request)
	if not request.user.is_authenticated():
		return error(format, "The user is not authenticated")
	try:
		elements=api.group.get_group_elements(group, request.user)
		data={"code": "200",
			  "elements": elements}
		return generateResponse(format, data, "group/elements")
	except:
		return error(format, "Unknown error")

def group_delete (request):
	format = getResponseFormat (request)
	if not request.user.is_authenticated():
		return error(format, "The user is not authenticated")
	if request.method == "POST":
		if ("groupid" in request.POST):
			group=request.POST['groupid']
			correct, message = api.group.delete(group)
			if correct:
				data = {'code'		 : '200',
						'description'  : 'Group deleted correctly',}
				return generateResponse(format, data, "ok")
			else:
				return error(format, message)			   
		else:
			return error(format, 'Missing parameters')
	else:
		return error(format, 'Need a POST petition')

def group_join (request):
	format = getResponseFormat (request)
	if not request.user.is_authenticated():
		return error(format, "The user is not authenticated")
	if request.method == "POST":
		if ("groupid" in request.POST) and ("userid" in request.POST):
			try:
				group=request.POST["groupid"]
				user=request.POST["userid"]
				correct, message = api.group.join(group, user)
				if correct:
					data={'code'		 : '200',
						  'description'  : 'Joined correctly',}
					return generateResponse(format, data, "ok")
				else:
					return error (format, message)
			except:
				return error(format, 'Unknown error occurred')			   
		else:
			return error(format, 'Missing parameters')
	else:
		return error(format, 'Need a POST petition')

def group_join_delete (request):
	format = getResponseFormat (request)
	if not request.user.is_authenticated():
		return error(format, "The user is not authenticated")
	if request.method == "POST":
		if ("groupid" in request.POST) and ("userid" in request.POST):
			try:
				group=request.POST["groupid"]
				user=request.POST["userid"]
				correct, message = api.group.unjoin (group, user)
				if correct:
					data = {'code'		 : '200',
							'description'  : 'Unjoined correctly',}
					return generateResponse(format, data, "ok")
				else:
					return error(format, message)
			except:
				return error(format, 'Unknown error occurred')			
		else:
			return error(format, 'Missing parameters')
	else:
		return error(format, 'Need a POST petition')

