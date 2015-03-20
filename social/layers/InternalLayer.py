#!/usr/bin/env python

# Copyright (C) 2009-2010 GSyC/LibreSoft, Universidad Rey Juan Carlos
# 
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see http://www.gnu.org/licenses/.
#
#  Author : Jose Gato Luis <jgato@libresoft.es>
#

from django.contrib.gis.geos import Point
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.measure import D 

from GIC.Channels.GenericChannel import *

from social.core.config import ALLOWED_SEARCH
from social.core.utils import get_person
from social.core.api_user import get_data as user_get_data
from social.core.api_layer import get_data as layer_get_data

import string

class InternalLayer (GenericChannel):
	
	MANDATORY_FIELDS = ["latitude", "longitude", "radius", "category"]
	CATEGORIES = [{"id" : "0", "name" : "all", "desc" : "All supported models in LibreGeoSocial"},
				  {"id" : "1", "name" : "photo", "desc" : "LibreGeoSocial GeoPhotoS"},
				  {"id" : "2", "name" : "note", "desc" : "LibreGeoSocial GeoNotes"},
				  {"id" : "3", "name" : "sound", "desc": "LibreGeoSocial GeoSounds"},
				  {"id" : "4", "name" : "video", "desc": "LibreGeoSocial GeoVideos"}]
	
	def __init__ (self, layer_id):
		self.options = {}
		self.layer_id = layer_id
		
	def get_info(self):
		layer_data = layer_get_data(self.layer_id)
		
		if layer_data == None:
			"""
			Maybe a virtual layer
			"""
			virtual_layer = user_get_data(self.layer_id)
			
			if virtual_layer != None:
				return "Virtual Layer: no description"
			else:
				return "No data"
		else:
			return layer_data["description"]
		   
	def get_categories(self):
		return self.CATEGORIES
		pass
			
	def set_mandatory_fields(self, dict):
	
		for field in self.MANDATORY_FIELDS:
			if not field in dict:
				return (False, field)
			else:
				self.options[field] = dict[field]
		  
		return (True, "")
	
	def set_options(self, options):
		
		success, result = self.set_mandatory_fields(options)
	
		if not success:
			return False, "\"%s\" parameter is mandatory " % (result)
		
		self.options["user"] = options["user"]
	
		return True, ""
	
	def _category_model(self):
		
		selected_category = self.options["category"]
		result = []
		
		for category in self.CATEGORIES:
			if selected_category == category["id"]:
				if category["id"] == "0":
					result = ALLOWED_SEARCH
				else:
					result = [category["name"]]
				break;
		
		return result
	
	def _serialize_results(self, results):
		"""
		After a searh we get an dictionary with arrays of models
		we will serialize it in a simple array of nodes
		"""
		node_list = []
		for model in results:
			for node in results[model]:
				node_list.append(node)
		
		return node_list
	def _do_search (self, type, fields, terms, layer_id, exact=False):
		"""
		Finds the objects in type whose fields include terms
		
		@param type: the model type
		@param fields: the fields that will be looked
		@param terms: the search terms
		@param layer_id: id of the layer to make the search
		@param exact: terms must be exact
		"""
		from social.core.models import LayerNodes, Person
		from django.contrib.gis.db.models.query import GeoQuerySet
		try:
			"""
			First of all we need to know if layer_id it is a real layer
			or virtual (user) layer
			"""
			virtual_layer = False
			user_layer = user_get_data(layer_id)
			
			if user_layer != None:
				virtual_layer = True
			
			result = type.objects.none()
			terms = string.split(terms)
			for f in fields:
				if virtual_layer:
					try:
						#print "virtual layer - ", type
						r = type.objects.filter(uploader = layer_id)
					except: #some types are not allowed in virtual layers, for example persons and return no results
						return result
				else:
					nodes_layer = LayerNodes.objects.get_nodes_for_layer(layer_id)
					r = type.objects.filter(id__in = nodes_layer)
					#if isinstance(node, Person):
					#	print "blblbl"
				for term in terms:
					if exact:
						r = r.__and__(type.objects.filter(**{"%s" % f: term}))
					else:
						r = r.__and__(type.objects.filter(**{"%s__icontains" % f: term}))
				result = result.__or__(r)
			
			return result
		except Exception, err:
			print err
			return None
			
	def _do_multi_search (self, types_fields, terms, layer_id, viewer=None, exact=False):
		"""
		This receives an array of dictionaries with types and terms 
		"""
		results = {}
		for tf in types_fields:
			if viewer:
				try:
					model_search = tf["type"].objects.allowed(viewer.id).__and__(self._do_search(tf["type"], tf["fields"], terms, layer_id, exact))
				except:
					return False
			else:
				model_search = self._do_search(tf["type"], tf["fields"], terms, exact)
			
			results[tf["type"]._meta.verbose_name] = model_search
		return results	

	def search(self, user, longitude, latitude, models, terms, layer_id, dist=0):
		"""
		Uses the search application and returns the results
		@param user: The user that makes the request, important for privacy
		@param longitude: longitude point to search around
		@param latitude: latitude point to search around
		@param models_fields: A list with the models
		@param terms: the search terms
		@param layer_id: id of the layer to make the search
		@param dist: the maximum distance from (longitude,latitude) point, if 0 
					 all matching nodes will be returned and longitude and latitude are ignored.
		 
		"""
		
		try:
			v = get_person(user)
		except:
			return []
		m_f=[]
		
		for model in models:
			if model in ALLOWED_SEARCH:
				try:
					model_type = ContentType.objects.get(name=model, app_label="core").model_class()
					m_f += [{"type": model_type, "fields": model_type.get_search_fields}]
				except Exception, err:
					print err
					pass
		
		results= self._do_multi_search(m_f, terms, layer_id, v )
		
		if results == False:
			return []
		
		#Now filter by distance if requested
		if float(dist) > 0:
			point = Point(float(longitude), float(latitude), srid=4326)
			for model in models:
				from django.db.models.query import EmptyQuerySet
				if not isinstance(results[model], EmptyQuerySet):
					results[model]=results[model].distance(point).order_by("distance"
						 ).filter(position__distance_lte=(point, D(km=float(dist))))
				else:
					results[model] = []
		
		"""
			 Serialize models to an unidimensional array, in order to extract the limits
			 and allow to create slides of information	
		"""
		node_list = self._serialize_results(results)
		
		return node_list


	def process(self):
		
		models = self._category_model()
		if len(models) > 0:
			results = self.search(self.options["user"], self.options["longitude"], self.options["latitude"], 
										   models, self.search_pattern, self.layer_id, self.options["radius"])
			return True, results
		else:
			return False, "Category not supported"
		

	