#!/usr/bin/env python
# -*- coding: utf-8 -*-


#  Copyright (C) 2009 GSyC/LibreSoft
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
#  Author : Roberto Calvo Palomino <rocapal _at_ libresoft _dot_ es>
#
#


from Auth import *
from Privacy import *
import simplejson
from MultiPart import *

class PhotosManager():


	format_json = "?format=JSON"
	url_create = "/social/photo/upload/" + format_json
	url_set_privacy = "/social/photo/%s/privacy/allow/" + format_json
	url_tag_photo = "/social/node/%s/tag/" + format_json
	url_img_photo = "/social/photo/%s/image/" 

	def __init__ (self):
		None


	def add_photo (self, photo):

		
		params = [ ('latitude' , str(photo.latitude)),
				   ('longitude' , str(photo.longitude)),
				   ('altitude' , str(photo.altitude)),
				   ('name' , photo.name),
				   ('description' , photo.description)
				 ]


		files = [ ('photo',
				   photo.path,
				   open(photo.path).read() )
				]


		content_type, body = encode_multipart_formdata(params, files)
				  


		data = Auth().do_petition(self.url_create, body, "POST", None, content_type)
		res = simplejson.load(data)

		if  (res['code'] != "200"):
			print photo.name
			print photo.description
			print photo.latitude
			print photo.longitude
			print photo.altitude
			print res
			return -1

		return res['id']


	def get_photo_img(self, photo_id):
		
		url = self.url_img_photo % (photo_id)
		
		data = Auth().do_petition(url, "", "GET" )
		
		if data.status == 200:
			return data.read()
		else:
			return None
		 
		
	def tag_photo (self, photo_id, tags):
		
		tag_params = ""
		
		for tag in tags:
			tag_params = tag_params + tag + " "
			
		params = urllib.urlencode ({'tags': tag_params})
		url = self.url_tag_photo % (photo_id)
		
		data = Auth().do_petition(url, params, "POST" )
		
		res = simplejson.load(data)
		
		if  (res['code'] != "200"):
			return -1
		
		return 0

	def set_privacy (self, photo_id, level):

		params = urllib.urlencode ({'role': Privacy.level [level]})
		url = self.url_set_privacy % (photo_id)
		
		data = Auth().do_petition(url, params, "POST" )
		
		res = simplejson.load(data)
		
		if  (res['code'] != "200"):
			return -1
		
		return 0

															
