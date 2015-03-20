#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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

from social.core.models import Person, Video
from GIC.Channels.GenericChannel import *
from django.contrib.gis.geos import Point

from Config import *

from urllib2 import urlopen, HTTPError, Request
import simplejson

class ChannelYoutube (GenericChannel):
	
	MANDATORY_FIELDS = ["latitude", "longitude", "radius", "category"]
	
	MEDIA_CONTENT_TYPES = { "flash" : "application/x-shockwave-flash",
						   "3gp" : "video/3gpp"}
	CATEGORIES = [{"id" : "0", "name" : "all", "desc" : "All supported categories in Youtube"},
				  {"id" : "1", "name" : "film", "desc" : "Videos about films"},
				  {"id" : "2", "name" : "animals", "desc" : "Videos about animals"},
				  {"id" : "3", "name" : "sports", "desc" : "Videos about sports"},
				  {"id" : "4", "name" : "travel", "desc": "Videos about travels"}]
	
	def __init__ (self):
		self.video_list = []
		self.options = {"search" : "",
						"category" : None,
						"latitude" : None,
						"longitude" : None,
						"radius" : None}
		
	def _category_type(self):
		
		selected_category = self.options["category"]
		result = False
		
		for category in self.CATEGORIES:
			if selected_category == category["id"]:
				if category["id"] == "0":
					result = ""
				else:
					result = category["name"]
				
				break;
		
		return result
	
		
	def get_categories(self):
		return self.CATEGORIES
	
	def get_info(self):
		return description
		
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
		  
		return (True, "")
		


	def _thumbnail_default(self, thumbnails):
		
		default = thumbnails[0]
		
		for thumb in thumbnails:
			url = str(thumb["url"])			
			if url.endswith("default.jpg") or url.endswith("hqdefault.jpg"):
				default = thumb 
		
		
		return thumb
	
	def _link_media_content(self, media_contents, type):
		
		media_content = media_contents[0]
		
		
		for media in media_contents:
			
			if media["type"] == type:
				media_content = media
		return media_content
		
	def process(self):

		request_url = youtube_api_url + "?q=" + self.options["search"]
		
		#be careful with categories, if the name begins with capital letter means
		#all the videos not in the selected category
		
		category = self._category_type()
		if category != False:
			if category != "":
				request_url = request_url + "&category=" + category
		else:
			return (False, "Category not supported")

		request_url = request_url + "&location=%s,%s!&location-radius=%skm&max-results=%s&alt=json&v=2" % (self.options["latitude"], self.options["longitude"], self.options["radius"], max_size_search)
		
		try:
			headers = { "X-GData-Key" : "key=" + youtube_developer_key }
			req = Request(request_url, None, headers)
			response = urlopen(req)
			youtube_response = response.read()
			feed_youtube = simplejson.loads(youtube_response)
		except HTTPError, e:
			print e
			return (False, e )
		
		if not "entry" in feed_youtube["feed"]:
			return True, self.video_list
		
		person = Person(pk = 666, position = Point(0.0, 0.0 , srid=4326)	)
		
		for video in feed_youtube["feed"]["entry"]:
			person.username = video["author"][0]["name"]["$t"]
			videoItem = Video( pk = 666,
							name = video["title"]["$t"],
							description = video["media$group"]["media$description"]["$t"],
							since = video["published"]["$t"],
							video_thumb_url = self._thumbnail_default (video["media$group"]["media$thumbnail"])["url"],
							info_url = video["media$group"]["media$player"]["url"],
							uploader = person,
							icon = channel_icon_url,
							type = "video",
							altitude = None )
			
			if "media$content" in video["media$group"]:
				videoItem.video_url = self._link_media_content(video["media$group"]["media$content"], 
																			self.MEDIA_CONTENT_TYPES["3gp"])["url"]
			
			try:
				geo = video["georss$where"]["gml$Point"]["gml$pos"]["$t"].split(" ")
				latitude = float(geo[0])										  
				longitude = float(geo[1])
				videoItem.position = Point(longitude, latitude, srid=4326)
			except Exception :
				videoItem.position = Point(0.0, 0.0 , srid=4326)

			self.video_list.append(videoItem)

		return True, self.video_list

#youtube = ChannelYoutube("")
#
#options = { "latitude" : 40.334943,
#			"longitude" : -3.872837,
#			"radius" : 100}
#youtube.set_options(options)
#youtube.proccess()