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
import fnmatch
import traceback

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from social.core.api_layer import get_data_by_name, create
from social.core.api_user import get_data, create_or_modify
from social.layers.config import LAYER_MANAGER, LAYER_DEFAULT, LAYER_DEFAULT_DESC
from social.core.utils import get_default_layer
from social.core.api_node import set_privacy_default
from os import path, listdir

from social.core.utils import get_person_by_name

"""
	Functions for layers in the DB management
"""

def _external_local_channels():

	try:
		channels_dir = path.join(settings.BASEDIR, "libs")
		
		if path.exists(channels_dir):
			channels = []
			for dir in listdir(channels_dir):
				if fnmatch.fnmatch(dir, 'channel*'):
					channel = path.join(channels_dir, dir)
					if path.isdir(channel):
						channels.append(dir) 
					
					
			return channels
		else:
			return None
		
	except ValueError, err:
		print err
		return None
	
def _create_layer(dict):
	result, layer_id = create(dict)
	if result:
		result, message = set_privacy_default(layer_id)
		
		if result:
			return result, layer_id
		else:
			return result, message
	else:
		return result, layer_id
	
def _test_channel(channel_object, channel):
	desc = channel_object.get_info()
	try:
		layer = get_data_by_name(channel)
		
		if layer == None:
			p = get_person_by_name(LAYER_MANAGER)
			print "Create layer ", channel
			layer_dict = {"name" : channel,
						  "description" : desc,
						  "layer_type" : "OFI",
						  "writeable" : 0,
						  "free" : 0,
						  "external" : 1,
						  "owner" : p.id,
						  "latitude" : "0",
						  "longitude" : "0",
						  "altitude" : "0" }
			return _create_layer(layer_dict)

	except MultipleObjectsReturned:
		print "Inconsistency Error:: More than one layer with name ", channel
	except Exception, err:
		print err


def create_default_layer():
	
	p = get_person_by_name(LAYER_MANAGER)
	layer_dict = {"name" : LAYER_DEFAULT,
					  "description" : LAYER_DEFAULT_DESC,
					  "layer_type" : "OFI",
					  "writeable" : 1,
					  "free" : 1,
					  "external" : 0,
					  "default" : 1,
					  "owner" : p.id,
					  "latitude" : "0",
					  "longitude" : "0",
					  "altitude" : "0" }
	
	return _create_layer(layer_dict)

	
def external_local_channels():
	import libs
	
	print "External layers"
	try:
		channels = _external_local_channels()
		
		print channels
		if channels == None:
			return False, "Error getting external channels from local directory"
		
		for channel in channels:
			channel_class = channel[0].upper() + channel[1:len(channel)]
			obj = __import__("libs.%s" % (channel), globals(), locals(), ["%s" % (channel_class)], 0)
			channel_object = eval ("obj." + channel_class + "." + channel_class + "()")
			_test_channel(channel_object, channel.replace("channel", ""))
		
		return True, ""
			
	except:
		traceback.print_exc()
		return False, "Unknown error"

def main():
	print "layers consistency"
	
	p = get_person_by_name(LAYER_MANAGER)
	
	if p == None:
		print "*** Warning: user for layer management (%s) does not exist " % (LAYER_MANAGER)
		print "*** Creating user"
		default_user = {"username" : LAYER_MANAGER,
						"password": "admin"}
		success, id = create_or_modify(default_user, False)
		
		if not success:
			print id
			print "Error creating user for layer management (%s) " % (LAYER_MANAGER)
			return
	
	success, response = external_local_channels()
	
	if not success:
		print "** Error with layer consistency", response
	else:
		try:
			default_layer = get_default_layer(None)
			if default_layer is not None:
				default_layer_name = default_layer["name"]
				
				if default_layer_name != LAYER_DEFAULT:
					print "** Error with the default layer"
			else:
				print "Default layer does not exist"
				print "Create default layer"
				print create_default_layer()
		except MultipleObjectsReturned:
			print "Inconsistency Error: More than one default layer"
		except Exception, err:
			print "Unknown error " , err
		
			

if __name__ == "__main__":
	main()
