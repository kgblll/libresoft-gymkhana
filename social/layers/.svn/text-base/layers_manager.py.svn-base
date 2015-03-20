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

		
import settings 

from social.layers.InternalLayer import InternalLayer
from settings import BASEDIR 
from social.core.models import Layer, Person, LayerNodes
from social.core.utils import get_person, get_person_by_name
from social.core.api_layer import get_data, is_external, create, delete, get_layer, get_default_layer
from social.core.api_user import get_data as user_get_data
from social.core.api_node import get_data as node_get_data
from social.core.api_node import set_dates as node_set_dates
from social.core.api_photo import get_image as photo_get_image
from social.core.models import Social_node

from custom_exceptions.layers_manager_exceptions import *
from social.core.custom_exceptions.social_core_exceptions import *

from os import path


ICONS_PATH = path.join(BASEDIR, "social", "site_media", "layers", "icons")



def layers_search(layers, search, options, multi_search = False):

	viewer = options["user"]

	if not multi_search:
		layers = [layers]
	
	contents = []
	for layer_id in layers:
		layer = get_layer_instance(layer_id, viewer)
		if layer != None:
			success, result = layer.set_options(options)
			if success:
				layer.set_search_pattern(search)
				success, result = layer.process()
				if success:
					contents = contents + result
				else:
					
					return success, result
			else:
				return success, result
		else:
			return False, "Error accessing to the layer" + layer_id
		
	return True, contents

def layers_categories(layer_id):
	
	layer = get_layer_instance(layer_id, None)
	
	if layer != None:
		return True, layer.get_categories()
	else:
		return False, "Error accessing to the layer" + layer_id
	
def layers_info(layer_id):
	
	layer = get_layer_instance(layer_id, None)
	
	if layer != None:
		return True, layer.get_info()
	else:
		return False, "Error accessing to the layer" + layer_id


def layers_icon(layer_id):
	
	try:
		layer = get_data(layer_id, None)
		if layer != None:
			try:
				url = path.join( ICONS_PATH , layer["name"] + ".png")
				if path.exists(url):
					image_data = open(url, "rb").read()
				else:
					url = path.join( ICONS_PATH , "lgs.png")
					image_data = open(url, "rb").read()
					
				return True, image_data 
			except :
				return False, "Could not retrieve layer %s icon" % (layer_id)
		else:
			
			"""
			Maybe the layer_id is the id of a virtual layer
			every user will have his own virtual layer. So,
			we will try to see if layer_id is an user_id
			"""
			
			virtual_layer = user_get_data(layer_id)
			
			if virtual_layer != None:
				
				if "avatar" not in virtual_layer:
					default_layer = get_default_layer()
					return layers_icon(default_layer.id)
				else:
					icon_id = virtual_layer["avatar"]["id"]
					icon_path = photo_get_image(icon_id, None, True)
					if icon_path != None:
						icon = open(icon_path, "rb").read()
						if icon != None:
							return True, icon
					
					return False, "Imposible to get layer's icon"
			
			return False, "Layer %s not supported." % (layer_id)
	except ValueError:
		return False, "Error retrieving icon"

def layers_change_icon(layer_id, viewer, params):
	from PIL import Image
	
	try:
		user = get_person(viewer)
	except:
		return False, "Not valid viewer"
	
	try:
		check_modify_layer(layer_id)
		layer = get_data(layer_id, None)
		
		if layer["uploader"]["id"] != user.id:
			raise LAYER_NOT_OWNER
		
		try:
			icon = Image.open(params["icon_data"])
			if not (icon.format in config.SUPPORTED_TYPES):
				return False, "The image type is not supported"

			icon.save( path.join(ICONS_PATH, layer["name"] + ".png") )
			
			return True
			
		except IOError, err:
			raise err
	except Layer_Does_Not_Exist, err:
		raise err
	except Layer_Perms, err:
		raise err
	
	return False

def layers_list(viewer, viewer_virtual_layer = False):
	from social.core.api_layer import get_all
	from django.contrib.gis.geos import Point
	
	try:
		user = get_person(viewer)
	except:
		return False, "Not valid viewer"

	layers = get_all(user)
	
	if layers is not None:
		if user.id != get_person_by_name("anonymous").id and viewer_virtual_layer:
			
			uploader = Person.objects.get(id = user.id)
			
							
			if user.first_name is not None and len(user.first_name) > 0: 
				user_name = user.first_name
				if user.last_name is not None and len(user.last_name) > 0:
					user_name = user_name + " " + user.last_name
			else: 
				user_name = user.username
			
			own_layer = Layer(pk = 666,
							name = user_name + " Personal Layer", 
							description = "Watch all your contents",
							id = user.id,
							writeable = True,
							layer_type = "USR",
							free = True,
							external = False,
							default = False,
							type = "layer",
							icon = "/social/layer/lgs/icon",
							uploader = uploader,
							position = Point ( float( uploader.get_dictionary()["position"]["longitude"]),
													float( uploader.get_dictionary()["position"]["longitude"]),
													srid=4326) )
																							
				
#			own_layer_dict = { "name" : user_name + " Personal Layer",
#							"description": "Watch all your contents",
#							"id" : user.id,
#							"writeable" : True,
#							"layer_type" : "USR",
#							"free" : True,
#							"external" : False,
#							"default" : False,
#							"type" : "layer",
#							"icon": "/social/layer/lgs/icon",
#							"uploader" : uploader,
#							"position" : user.get_dictionary()["position"]
#							}
			
			layers_list = []
			layers_list.append(own_layer)
			
			for layer in layers:
				layers_list.append(layer)
		
			
			
			return True, layers_list
		return True, layers
	else:
		return False, layers


def _get_channel_intance(layer_id):
	"""
	 retuns an instance of the channel manager
	 regarding his identification in the layers
	 data base
	"""
	layer = get_data(layer_id, None)
	
	if layer == None:
		return layer
	else:
		channel_name = layer["name"]
			
		channel_class = "Channel" + channel_name[0].upper() + channel_name[1:len(channel_name)]
		obj = __import__("libs.channel%s" % (channel_name), globals(), locals(), [str(channel_class)], 0)
		channel_object = eval ("obj." + channel_class + "." + channel_class + "()")
		
		return channel_object

def get_layer_instance(layer_id, viewer = None):
	
	layer = get_data(layer_id, viewer)
	try:
		if layer != None:
			external = layer["external"]
			
			if external:
				channel = _get_channel_intance(layer_id)
				if channel != None:
					return channel
				else:
					return None
			else:
				internal_layer = InternalLayer(layer_id)
				
				if internal_layer != None:
					return internal_layer
				else:
					return None
		else:
			"""
			Maybe the layer_id is the id of a virtual layer
			every user will have his own virtual layer. So,
			we will try to see if layer_id is an user_id
			"""
			
			virtual_layer = user_get_data(layer_id,viewer)
			
			if virtual_layer != None:
				virtual_layer = InternalLayer(virtual_layer["id"])
				if virtual_layer!= None:
					return virtual_layer
				
			return None
	except Exception, err:
		print err
		return None

def layers_create(dict):
	
	return create(dict)

def layers_delete(layer_id, user_id):
	try:
		layer = get_layer_instance(layer_id, user_id)
		if layer != None:
			return delete(layer_id, user_id)
		else:
			return False, "Error accessing to the layer %i" % (layer_id) 
	except:
		return False, "Error accessing to the layer %i" % (layer_id) 
	

def _check_layer_state(layer_id, create_node = False):
	"""
		check the layer state regarding:
		* existence
		* external
		* writeable
	"""
	
	layer_instance = get_layer(layer_id)
	
	if layer_instance == None:
		raise LAYER_DOES_NOT_EXIST
	
	if layer_instance.external == True:
		if create_node:
			raise LAYER_EXTERNAL_NOT_CREATE_NODES
		elif create_node is False:
			raise LAYER_EXTERNAL_NOT_DELETE_NODES
		else:
			raise LAYER_EXTERNAL_NOT_MODIFY
	
	if layer_instance.writeable == False:
		raise LAYER_NOT_WRITE 
	

def check_modify_layer(layer_id):
	"""
		Check the conditions to modify a layer
	"""
	
	_check_layer_state(layer_id, None)
	
	return True

def check_node_create(layer_id):
	"""
		Check the conditions to create a new node in a layer
	"""
	
	_check_layer_state(layer_id, True)
	
	return True
	
def check_node_delete(layer_id, node_id):
	"""
		Check the conditions to delate a node from a layer
	"""
	import types
	
	_check_layer_state(layer_id)
	
	if not isinstance(node_id, types.IntType):
		node_id = int(node_id) 
		
	if node_id not in LayerNodes.objects.get_nodes_for_layer(layer_id):
		raise LAYER_NOT_NODE
	
	return True

def check_node_data(layer_id, node_id):
	"""
		Check the conditions to access a node's data
	"""
	import types

	#allowed virtual layers
	
	layer_instance = get_layer_instance(layer_id)
	
	if layer_instance == None:
		raise LAYER_DOES_NOT_EXIST
	
	if not isinstance(node_id, types.IntType):
		node_id = int(node_id) 
		
	if node_id not in LayerNodes.objects.get_nodes_for_layer(layer_id):
		node = Social_node.objects.get(id=node_id).get_node()
		uploader_id = node.uploader.id
		
		#if uploader_id == layer_id we are using a virtual layer
		if not uploader_id == int(layer_id):
			raise LAYER_NOT_NODE
	
	return True

def get_node_data(layer_id, node_id, user_id):
	
	try:
		check_node_data(layer_id, node_id)
		node = node_get_data(node_id, user_id)
		return node
	except Layer_Does_Not_Exist, err:
		raise err
	except Layer_Node, err:
		raise err
	except Exception, err:
		raise err
	

def get_node_image(layer_id, node_id, user_id, size=None, thumb=False):
	
	try:
		check_node_data(layer_id, node_id)
		node = Social_node.objects.get(id=node_id)
		type = node.get_node().type
		
		try:
			api = __import__("social.core.api_%s" % (type), globals(), locals(), ["get_image"], 0)
			get_image = api.get_image
		except:
			raise NODE_NOT_IMAGE 
		
		if thumb:
			image_path = get_image(node_id, thumb=True, viewer=user_id)
		else:
			if size=="medium":
				image_path = get_image(node_id, (500, 500), viewer=user_id)
			elif size=="small":
				image_path = get_image(node_id, (250, 250), viewer=user_id)
			elif size=="large":
				image_path = get_image(node_id, (800, 800), viewer=user_id)
			else:
				image_path= get_image(node_id, viewer=user_id)
		
		if image_path == None:
			return None
		
		image_data = open(image_path, "rb").read()

		return image_data
	except Layer_Does_Not_Exist, err:
		raise err
	except Layer_Node, err:
		raise err
	except Exception, err:
		raise err

def get_node_image_path(layer_id, node_id, user_id, size=None, thumb=False):

        try:
                check_node_data(layer_id, node_id)
                node = Social_node.objects.get(id=node_id)
                type = node.get_node().type

                try:
                        api = __import__("social.core.api_%s" % (type), globals(), locals(), ["get_image"], 0)
                        get_image = api.get_image
                except:
                        raise NODE_NOT_IMAGE

                if thumb:
                        image_path = get_image(node_id, thumb=True, viewer=user_id)
                else:
                        if size=="medium":
                                image_path = get_image(node_id, (500, 500), viewer=user_id)
                        elif size=="small":
                                image_path = get_image(node_id, (250, 250), viewer=user_id)
                        elif size=="large":
                                image_path = get_image(node_id, (800, 800), viewer=user_id)
                        else:
                                image_path= get_image(node_id, viewer=user_id)

                return image_path
        except Layer_Does_Not_Exist, err:
                raise err
        except Layer_Node, err:
                raise err
        except Exception, err:
                raise err


def get_node_sound(layer_id, node_id, user_id):
	
	try:
		check_node_data(layer_id, node_id)
		node = Social_node.objects.get(id=node_id)
		type = node.get_node().type
		
		try:
			api = __import__("social.core.api_%s" % (type), globals(), locals(), ["get_sound_file"], 0)
			get_sound_file = api.get_sound_file
		except:
			raise NODE_NOT_SOUND 
		
		sound_path = get_sound_file(node_id, user_id)
		if sound_path == None:
			return None
		
		sound_data = open(sound_path, "rb").read()

		return sound_data
	except Layer_Does_Not_Exist, err:
		raise err
	except Layer_Node, err:
		raise err
	except Exception, err:
		raise err

def get_node_video(layer_id, node_id, user_id):
	
	try:
		check_node_data(layer_id, node_id)
		node = Social_node.objects.get(id=node_id)
		type = node.get_node().type
		
		try:
			api = __import__("social.core.api_%s" % (type), globals(), locals(), ["get_video_file"], 0)
			get_video_file = api.get_video_file
		except:
			raise NODE_NOT_VIDEO
		
		video_path = get_video_file(node_id, user_id)
		if video_path == None:
			return None
		
		video_data = open(video_path, "rb").read()

		return video_data
	except Layer_Does_Not_Exist, err:
		raise err
	except Layer_Node, err:
		raise err
	except Exception, err:
		raise err

def get_node_layers(node_id, user_id):
	
	try:
		
		node = node_get_data(node_id, user_id)
		
		if node == None:
			raise NODE_NOT_EXIST_OR_PERM
		
		layers_ids = LayerNodes.objects.get_layers_for_node(node_id)
		
		layers_list = []
		for layer in layers_ids:
			layer_data = get_data(layer)
			if not layer_data == None:
				layers_list.append(layer_data)
		
		print layers_list
		return layers_list
	except Layer_Does_Not_Exist, err:
		raise err
	except Layer_Node, err:
		raise err
	except Exception, err:
		raise err
	
	
def set_node_dates(layer_id, node_id, user_id, avaliable_from, avaliable_to):
	
	try:
		check_node_data(layer_id, node_id)
		node_set_dates (node_id, avaliable_from, avaliable_to)
		
	except Layer_Does_Not_Exist, err:
		raise err
	except Layer_Node, err:
		raise err
	except Exception, err:
		raise err

def layer_is_external(layer_id, user_id):
	
	return is_external(layer_id, user_id)