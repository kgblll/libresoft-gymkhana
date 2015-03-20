#
#  Copyright (C) 2010 GSyC/LibreSoft
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
#    Author : Raul Roman Lopez <rroman __at__ libresoft __dot__ es>
#

from social.layers.layers_manager import layers_search, layers_categories, layers_list, get_node_image
from social.core.api_layer import is_external
from social.core import api
from social.rest.forms import ComparePhotoForm
from social.rest.utils import error, get_authenticated_user
from social.privacy2.utils import test_privacy_field_over_nodes
from social.layers import layers_manager
from ComparisonManager import ComparisonManager

from xml.dom import minidom
from xml.dom.minidom import Document, parseString

from django.http import HttpResponse
from format.utils import  getResponseFormat, generateResponse
from os import remove

from multiprocessing import Process, Value, Condition, Lock, Manager, Semaphore

def _getLGSLayer(user):
	_id = None
	try:
		success, response = layers_list(user, False)
		
		if success:
			node_list = response
			
			
			try:
				node_list = test_privacy_field_over_nodes(node_list, user)
			except :
				print "**** error getting privacy over results"
				return _id
			
			for layer in node_list:
				if (layer["name"] == "lgs") or (layer["name"] == "LibreGeoSocial"):
					_id = layer["id"]
					break
			
			return _id
	except Exception,e :
		print "****", e
		return _id

def _getPhotosCategory(layer_id):
	_id = None
	success, response = layers_categories(layer_id)
	
	if success:
		for category in response:
			if category["name"] == "photo":
				_id = category["id"]
				break;
	return _id

def _getPhotoNodes(user, layer_id, latitude, longitude, radius):
	category = _getPhotosCategory(layer_id)
	if not category:
		return None
	
	options = {"category": str(category),
			"user": user,
			"layer_id": layer_id,
			"search": "",
			"latitude": latitude,
			"longitude": longitude,
			"radius": radius
		}
	success, response = layers_search(layer_id, "", options)
	
	if success:
		node_list = response
		
		if not is_external(layer_id):
			try:
				node_list = test_privacy_field_over_nodes(node_list, user)
			except:
				return None
		return node_list
	return None

def _analizePhotos(photo, data, user, layer_id, matched, photo_id, goodness, lock, lock2, sem):
	print user
	
	lock2.acquire()
	image_path = layers_manager.get_node_image_path(layer_id, photo["id"], user, size="large")
	lock2.release()
	
	sm = ComparisonManager()
	_matched, _goodness = sm.compareTwoPhotos(image_path, None, data)
	
	# Shared variables
	lock.acquire()
	if _matched:
		if _goodness < goodness.value:
			photo_id.value = photo["id"]
			if photo["description"].find("linkto://") > -1 :
				photo_id.value = int(photo["description"].split("linkto://")[1].split("\n")[0])
			matched.value = _matched
			goodness.value = _goodness
	sem.release()
	lock.release()

def _getBestPhoto(user, layer_id, photos_list, path2):
	data = ComparisonManager().extractSURFPoints(path2)
	
	# Shared variables
	matched = Value('i', -1)
	photo_id = Value('i', -1)
	goodness = Value('d', 10000.0)
	
	# Multiprocessing control variables
	manager = Manager()
	lock = manager.Lock()
	lock2 = manager.Lock()
	sem = manager.Semaphore(4) # For a 4-core machine
	p_list = []
	
	# launching children
	for photo in photos_list:
		sem.acquire()
		p = Process(target=_analizePhotos, args=(photo, data, user, layer_id, matched, photo_id, goodness, lock, lock2, sem))
		p.start()
		p_list.append(p)
	
	# waiting for children
	for proc in p_list:
		proc.join()
	
	if matched.value < 0:
		return None
	return {"code": "200", 
			"layer_id": layer_id, 
			"photo_id": photo_id.value, 
			"matched": matched.value, 
			"goodness": goodness.value
		 }

def compareSocialPhotos(request):
	''' This function needs the user position < soon: and his orientation >'''
	format = getResponseFormat (request)
	
	if request.method != 'POST':
		return error(format, "Unsupported method %s" % (request.method))
	
	user = get_authenticated_user (request.user, allow_anonymous = True)
	if user == None:
		return error(format, "The user is not authenticated")

	
	if "layer_id" in request.POST:
		layer_id = request.POST["layer_id"]
	else:
		layer_id = _getLGSLayer(user)
	
	if not layer_id:
		return error(format, "No LibreGeoSocial layer available at this moment")
	
	photo_category_id = _getPhotosCategory(layer_id)
	if not photo_category_id:
		return error(format, "No category of photos in this layer")
	
	photos_list = _getPhotoNodes(user, layer_id, request.POST["latitude"], request.POST["longitude"], request.POST["radius"])
	
	path2 = '/tmp/' + user.username + '_temp.jpg'
	arch=open(path2,'w')
	arch.writelines(request.FILES["photo"].read(request.FILES["photo"].size))
	arch.close()
	
	result = _getBestPhoto(user, layer_id, photos_list, path2)
	remove(path2)
	print "Bye"
	if result:
		return generateResponse(format, result, "compareSocialPhotos")
	return error(format, "No match")

def compareTwoPhotos(request):
	''' This function compares two photo nodes given their IDs'''
	format = getResponseFormat (request)
	
	if request.method != 'GET':
		return error(format, "Unsupported method %s" % (request.method))
	
	user = get_authenticated_user (request.user, allow_anonymous = True)
	if user == None:
		return error(format, "The user is not authenticated")

	if "layer_id" in request.GET:
		layer_id = request.GET["layer_id"]
	else:
		layer_id = _getLGSLayer(user)
		if not layer_id:
			return error(format, "No LibreGeoSocial layer available at this moment")
	
	
	photo1_id = request.GET["photo1"]
	photo2_id = request.GET["photo2"]
	
	photo1 = layers_manager.get_node_image_path(layer_id, photo1_id, user, size="large")
	photo2 = layers_manager.get_node_image_path(layer_id, photo2_id, user, size="large")
	
	if (not photo1) or (not photo2):
		return error(format, "Photos not available")
	
	sm = ComparisonManager()
	matched, goodness = sm.compareTwoPhotos(photo1, photo2)
	
	if not matched:
		return error(format, "No match")
	
	data = {"code"   : "200",
			"matched"   : matched,
			"goodness"   : goodness
		}				
	return generateResponse(format, data, "compareNodes")

	
	

