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
#	Author : Jose Gato Luis <jgato@libresoft.es>
#

from django.contrib.gis.geos import Point

from models import Layer, Person
from utils import get_person, check_layer_dict, set_default_icon, get_default_layer
from social.privacy.exceptions import PermissionError
from social.core.api_node import delete as delete_node

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

def create(layer):
	"""
	Creates a new layer
	"""
	from social.privacy2.models import Privacy
	try:
		layer, message = check_layer_dict(layer)
		if layer == None :
			return False, message
		point = Point(float(layer["longitude"]), float(layer["latitude"]), srid=4326)
		try:
			p = Person.objects.get(pk=layer["owner"])
		except:
			return False, "Not valid uploader"
		
		try:
			if not "default" in layer:
				layer["default"] = False
				
			layer = Layer(name = layer["name"], 
						  description = layer["description"], 
						  layer_type = layer["layer_type"],
						  writeable = layer["writeable"],
						  free = layer["free"],
						  external = layer["external"],
						  default = layer["default"],
						  uploader = p,
						  position = point,
						  altitude = layer["altitude"])
			
			if layer.icon is None or layer.icon == "":
				set_default_icon(layer)
			layer.save()
			
			return True, layer.id
			
		except ValueError:
			print ValueError
			return False, "Layer can't be created"
	except ValueError:
		print ValueError
		return False, "Unknown error"

def get_all(viewer=None):
	"""
	Returns an array with all the Layers
	"""
	try:
		v=get_person(viewer)
		
		if v != None:
			layers = Layer.objects.allowed(v.id).distance(v.position).order_by("distance")
		elif viewer == None:
			layers = Layer.objects.all()
			
		return layers
	except Exception, err:
		return None

	
def get_data_by_name(name, viewer = None):
	"""
	Returns a Layer ditct  using the layer name
	"""
	try:
		v = get_person(viewer)
		l = Layer.objects.get(name = name)
		return l.get_dictionary(viewer=v)
	except ObjectDoesNotExist:
		print "Layer %s does not exist" % (name)
		return None
	except MultipleObjectsReturned:
		print "More than one layer with name %s" % (name)
		raise MultipleObjectsReturned
	
def get_data(layer_id, viewer=None):
	"""
	Returns the details (dict) for a layer
	"""
	try:
		v = get_person(viewer)
		l = Layer.objects.get(id=layer_id)
		return l.get_dictionary(viewer=v)
	except ObjectDoesNotExist:
		print "Layer %s does not exist" % (layer_id)
		return None
	except MultipleObjectsReturned:
		print "More than one layer with name" % (layer_id)
		raise MultipleObjectsReturned
	except Exception, err:
		print err
		return None

def get_layer(layer_id, viewer=None):
	"""
	Returns the layer object
	"""
	try:
		v = get_person(viewer)
		l = Layer.objects.get(id=layer_id)
		return l
	except ObjectDoesNotExist:
		print "Layer %s does not exist" % (layer_id)
		return None
	except MultipleObjectsReturned:
		print "More than one layer with name" % (layer_id)
		raise MultipleObjectsReturned
	except Exception, err:
		print err
		return None

def get_default_layer(viewer = None):
	"""
	Returns the default layer in the system
	"""
	
	try:
		v = get_person(viewer)
		l = Layer.objects.get(default = True)
		return l
	except ObjectDoesNotExist:
		print "No default layer in the system"
		return None
	except MultipleObjectsReturned:
		print "More than one layer default layer"
		raise MultipleObjectsReturned
	except Exception, err:
		print err
		return None


def get_for_user(user_id, from_limit, to_limit, viewer=None):
	"""
	Returns all the user's layers
	"""
	pass
	
def delete(layer_id, user_id):
	"""
	Delete the layer layer_id
	"""
	try:
		default_layer = get_default_layer(user_id)
		
		if default_layer.id == layer_id:
			return False, "Default layer can not be deleted"
		
		return delete_node(layer_id, user_id)
		
	except ObjectDoesNotExist:
		return False, "Error in the system: default layer does not exist"
	except MultipleObjectsReturned:
		return False, "Error in the system: more than one default layer"
	
	
	
def is_external(layer_id, viewer = None):
	"""
	Returns the details for a note
	"""
	try:
		v = get_person(viewer)
		l = Layer.objects.get(id=layer_id)
		return l.get_dictionary(viewer=v)["external"]
	except Exception, err:
		print err
		return None
	