#
# Copyright (C) 2009-2010 GSyC/LibreSoft, Universidad Rey Juan Carlos
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

import hashlib
import random

from social.privacy2.config import privacy 
from config import DEFAULT_NODE_ICON
from django.contrib.gis.geos import Point
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from social.core.config import EXPIRATION_DATE_FORMAT

def rand_name():
	m = hashlib.md5()
	m.update(str(random.random()))
	return m.hexdigest()

	
def get_person_by_name(name):
	"""
	Returns a Person object using the username
	"""
	from models import Person
	try:
		return Person.objects.get(username = name)
	except Exception, e:
		print e
		return None

def get_person(user):
	"""
	Returns a Person object for User object "user" or None if not exists
	"""
	from models import Person
	try:
		return Person.objects.get(id=user.id)
	except:
		return None

def add_node_to_group(node, group, data=[]):
	"""
	Receives the models Social_node and Group and create a new Member
	"""
	from models import Membership
	if Membership.objects.get_relation(node1=node, node2=group) == None:
		member=Membership(node1=node, node2=group)
		member.save()
		return True
	else:
		return False

def add_person_to_group(person, group, data=[]):
	"""
	Receives the models Person and Group and create a new Member
	"""
	return add_node_to_group(person, group, data)

def check_person_dict(person):
	#Check needed fields
	if "username" not in person:
		return None, "username field needed"
	if "password" not in person:
		return None, "password field needed"
	#Return ok
	return person, "Ok"

def check_note_dict(note):
	from social.rest.notes import NOTE_FIELDS_COMPLETE
	#Check needed fields
	
	for field in NOTE_FIELDS_COMPLETE:
		if field not in note:
			return None, "%s field needed" % (field)

	if "altitude" not in note:
		note["altitude"]="0"
	if "avaliable_from" not in note:
		note["avaliable_from"] = None
	if "avaliable_to" not in note:
		note["avaliable_to"] = None
		
	return note, "Ok"
	
def check_group_dict(group):
	#Check needed fields
	if "groupname" not in group:
		return None, "groupname field needed"
	#Check optional fields
	if "latitude" not in group:
		group["latitude"]="0"
	if "longitude" not in group:
		group["longitude"]="0"
	if "radius" not in group:
		group["radius"]="0"
	if "altitude" not in group:
		group["altitude"]="0"
	#Return ok
	return group, "Ok"

def check_photo_dict(photo):
	from social.rest.photos import PHOTO_FIELDS_COMPLETE
	#Check needed fields
	
	for field in PHOTO_FIELDS_COMPLETE:
		if field not in photo:
			return None, "%s field needed" % (field)

	if "altitude" not in photo:
		photo["altitude"]="0"
	if "avaliable_from" not in photo:
		photo["avaliable_from"] = None
	if "avaliable_to" not in photo:
		photo["avaliable_to"] = None

	return photo, "Ok"

def check_sound_dict(sound):
	#Check needed fields
	if "sound_name" not in sound:
		return None, "sound_name field needed"
	if "sound_data" not in sound:
		return None, "sound_data field needed"
	if "description" not in sound:
		return None, "description field needed"
	if "latitude" not in sound:
		return None, "latitude field needed"
	if "longitude" not in sound:
		return None, "longitude field needed"
	if "uploader" not in sound:
		return None, "uploader field needed"
	#Check optional fields
	if "radius" not in sound:
		sound["radius"]=""
	if "altitude" not in sound:
		sound["altitude"]="0"
	if "avaliable_from" not in sound:
		sound["avaliable_from"] = None
	if "avaliable_to" not in sound:
		sound["avaliable_to"] = None

	return sound, "Ok"

def check_video_dict(video):
	from social.rest.videos import VIDEO_FIELDS_COMPLETE
	#Check needed fields
	
	for field in VIDEO_FIELDS_COMPLETE:
		if field not in video:
			return None, "%s field needed" % (field)

	if "altitude" not in video:
		video["altitude"]="0"
	if "avaliable_from" not in video:
		video["avaliable_from"] = None
	if "avaliable_to" not in video:
		video["avaliable_to"] = None

	return video, "Ok"

def check_video_supported(video):
	
	return True

def check_layer_dict(layer):
	from social.rest.layers import LAYER_FIELDS_COMPLETE
	#Check needed fields
	
	for field in LAYER_FIELDS_COMPLETE:
		if field not in layer:
			return None, "%s field needed" % (field)

	if "altitude" not in layer:
		layer["altitude"]="0"

	return layer, "Ok"

def get_correct_size(max_w, max_h, w, h):
	"""
		Returns the correct width and heigth with the same proportion as
		w,h tuple and not exceeding the maximum w and h indicated
	"""
	new_ratio = float(max_h)/float(max_w)
	ratio = float(h)/float(w)
	if ratio>new_ratio:
		return int(max_h/ratio), max_h
	else:
		return max_w, int(max_w*ratio)

def get_fields_for_groups(obj, groups):
	"""
	Returns  all the fields for the groups in the list using the privacy 
	configuration file
	
	@param groups: A list of groups
	@param obj: The object requested 
	
	@return: The fields in the groups  
	"""
	try:
		p_obj=privacy[obj.__module__][obj.__class__.__name__]
	except ValueError:
		print ValueError
		return []
	
	fields=[]
	for g in groups:
		try:
			fields+=p_obj[g]
		except:
			pass
	return fields

def get_group_for_field(obj, field):
	"""
	Returns the group where the field is in
	
	@param obj: The requested object
	@param field: The field  
	
	@return: The group for the field
	"""
	try:
		p_obj=privacy[obj.__module__][obj.__class__.__name__]
	except Exception, err:
		print err
		return None
	for g in p_obj.keys():
		if field in p_obj[g]:
			return g;
	return None

def set_default_icon(obj):
	
	obj.icon = DEFAULT_NODE_ICON
 
 #####
 # tools to order list by distance
 #####
 
def distance(point1, point2):
	import math
	
	lat1 = point1.get_y()
	long1 = point1.get_x()
	lat2 = point2.get_y()
	long2 = point2.get_x()
	
	mean_earth_radius = 6371.009 #km
	# Convert latitude and longitude to 
	# spherical coordinates in radians.
	degrees_to_radians = math.pi/180.0
		
	# phi = 90 - latitude
	phi1 = (90.0 - lat1)*degrees_to_radians
	phi2 = (90.0 - lat2)*degrees_to_radians
		
	# theta = longitude
	theta1 = long1*degrees_to_radians
	theta2 = long2*degrees_to_radians
		
	# Compute spherical distance from spherical coordinates.
		
	# For two locations in spherical coordinates 
	# (1, theta, phi) and (1, theta, phi)
	# cosine( arc length ) = 
	#	sin phi sin phi' cos(theta-theta') + cos phi cos phi'
	# distance = rho * arc length
	
	cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
		   math.cos(phi1)*math.cos(phi2))
	try:
		arc = math.acos( cos )
	except:
		arc = 0.0

	# Remember to multiply arc by the radius of the earth 
	# in your favorite set of units to get length.
	return arc * mean_earth_radius	   

def _insert_ordered (list, elem, value):
	
	ordered = []
	
	if len(list) == 0:
		ordered.append(elem)
	else:
		for n in list:
			if value != None and value < n["dist"]:
				ordered.append(elem)
				ordered.append(n)
				value = None
			else:
				ordered.append(n)
			
		#still not placed = last element
		if value != None:
			ordered.append(elem)

	return ordered
	
def order_by_distance(list, longitude, latitude):
	
	p1 = Point(float(longitude), float(latitude), srid=4326)
	ordered_list = []
	nodistance_list = []
	for node in list:
		if "position" in node:
			position = node["position"]
			p2 = Point(float(position["longitude"]), float(position["latitude"]), srid=4326)
			node["dist"] = distance(p1,p2)
			ordered_list = _insert_ordered(ordered_list, node, node["dist"])
		else:
			nodistance_list.append(node)
	return ordered_list + nodistance_list  

def get_default_layer(viewer = None):
	"""
		Returns the default layer, only one layer should be the default one
	"""
	from models import Layer
	
	try:
		v=get_person(viewer)
		l = Layer.objects.get(default = True)
		return l.get_dictionary(viewer=v)
	except ObjectDoesNotExist:
		print "Default layer does not exist"
		return None
	except MultipleObjectsReturned:
		print "More than one default layer"
		raise MultipleObjectsReturned

def get_dict_datetime(dict):
	import datetime
	from social.core.custom_exceptions.social_core_exceptions import DATE_TIME_FORMAT_ERROR

	if dict["avaliable_from"] == "" or dict["avaliable_to"] == "":
		return None, None
		
	avaliable_from = None
	avaliable_to = None
	try:
		if dict["avaliable_from"] is not None:
			avaliable_from = datetime.datetime.strptime(dict["avaliable_from"], EXPIRATION_DATE_FORMAT)
		if dict["avaliable_to"] is not None:
			avaliable_to = datetime.datetime.strptime(dict["avaliable_to"], EXPIRATION_DATE_FORMAT)
	except:
		raise DATE_TIME_FORMAT_ERROR
	
	return avaliable_from, avaliable_to 

def check_expiration_time(date):
	import datetime
	from social.core.custom_exceptions.social_core_exceptions import DATE_TIME_FUTURE
	
	if date < datetime.datetime.today():
		raise DATE_TIME_FUTURE
	
def check_later_date(date_from, date_to):
	from social.core.custom_exceptions.social_core_exceptions import DATE_TIME_NOT_LATER
	
	if date_to <= date_from:
		raise DATE_TIME_NOT_LATER
	
def get_visible_dates_interval(dict):

	avaliable_from, avaliable_to = get_dict_datetime(dict)
	
	if avaliable_to is not None:
		check_expiration_time(avaliable_to)	
		if avaliable_from is not None:
			check_later_date(avaliable_from, avaliable_to)

	return avaliable_from, avaliable_to
		