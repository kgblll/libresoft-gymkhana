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
#	Author : Jose Antonio Santos Cadenas <jcaden __at__ gsyc __dot__ es>
#

import __aux__ as aux

from social.core.utils import get_person

import social.core.models

def get_all_roles_names():
	ret_roles = []
	#TODO: Check other roles and names
	return ret_roles

def get_perm_names():
	from social.privacy2.models import PRIVACY_CHOICES
	ret_perm = []
	for p in PRIVACY_CHOICES:
		ret_perm.append(p[1])
	return ret_perm

def is_allowed(req_obj, requester, field=None):
	from social.privacy2.models import Privacy, Privacy_field
	from social.core.models import Friendship

	try:
		if not field == None:
			p, created = Privacy_field.objects.get_or_create(node=req_obj, field=field)
		else:	
			p, created = Privacy.objects.get_or_create(node=req_obj)
		if created:
			p.save()
		owner = req_obj.get_owner()
		if requester == owner:
			return True
		if p.friends_privacy == 3:
			return True
		elif p.friends_privacy == 2:
			return Friendship.objects.are_friends_of_friends(requester, owner)
		elif p.friends_privacy == 1:
			return Friendship.objects.are_friends(requester, owner)
		else:
			return False

		#Todo check roles and groups
	except:
		return True

def get_object_status(req_obj):
	from social.privacy2.models import Privacy
	from social.privacy2.models import PRIVACY_CHOICES

	p, created = Privacy.objects.get_or_create(node=req_obj)
	if created:
		print "Created"
		p.save()
	response={"full":[], "forbidden": [], "fields_allowed": {},
			  "fields_forbidden": {},}
	for field in aux.get_groups(req_obj):
		response["fields_allowed"][field]=[]
		response["fields_forbidden"][field]= []
		
	for c in PRIVACY_CHOICES:
		if p.friends_privacy == c[0]:
			response["full"].append(c[1])
	response["fields_allowed"]["basic"]= response["full"]+[]
	response["fields_forbidden"]["basic"]=  response["forbidden"]+[]
	return response

#Temp functions

def get_privatizable_fields():
	return ["position"]

def is_privatizable_field(field):
	if field == "position":
		return True
	else:
		return False

def get_fields(req_obj, requester):
	"""
	This function will return an array with the name of the allowed fields of req_obj
	for the requester user.
	
	@param req_obj: The requested object that will be checked
	@param requester: The user that wants to access to the req_obj  
	
	@return: An array with all the allowed fields, if the array is empty means
			 that the requester has access to basic fields but no to other fields.
			 If return None means no access to the object
	"""
	allowed = []
	for f in aux.get_groups(req_obj):
		if (not is_privatizable_field(f)) or is_allowed(req_obj, requester, f):
			allowed.append(f)
	return allowed
	
	
def get_perm_value(perm_string):
	from social.privacy2.models import Privacy, PRIVACY_CHOICES
	
	perm_val = -1
	for c in PRIVACY_CHOICES:
		if perm_string == c[1]:
			perm_val = c[0]
			
	return perm_val

def set_perm(obj, perm):
	from social.privacy2.models import Privacy, PRIVACY_CHOICES
	p, created = Privacy.objects.get_or_create(node=obj)
	perm_val = -1
	for c in PRIVACY_CHOICES:
		if perm == c[1]:
			perm_val = c[0]
	if perm_val != -1:
		p.friends_privacy = perm_val
		p.save()
		return True
	return False

def set_perm_field(obj, field, perm):
	from social.privacy2.models import Privacy_field
	
	perm_value = get_perm_value(perm)
  
	if is_privatizable_field(field) and perm_value != -1:
		p, created = Privacy_field.objects.get_or_create(node=obj)
		p.field = field
		p.friends_privacy = perm_value
		p.save()
		return True
	
	return False
				
def test_privacy_field_over_nodes(nodes, viewer):
	"""
		Test privacy over the nodes regarding viewer.
		Returns the nodes list with the allowed fields
		regarding viewer
	"""	
	from social.privacy.exceptions import PermissionError
	from social.core.models import Social_node
	try:
		user = get_person(viewer)
		result = []
		for node in nodes:
			if node.id != None:
				try:
					result += [node.get_node().get_dictionary(user)]
				except PermissionError:
					print "permission error"
					pass
			else: #we dont care of privacy with no social nodes (probably external sources)
				result.append(node.get_node().get_dictionary())
		return result
	except Exception, err:
		print err
		return []
	