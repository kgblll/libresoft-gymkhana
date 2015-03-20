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

import sys 

from format.utils import  getResponseFormat, generateResponse
from social.core import api
from social.core.api_layer import get_data as layer_get_data
from social.rest.forms import VideoForm
from social.layers.layers_manager import check_node_create
from social.layers.custom_exceptions.layers_manager_exceptions import *
from social.core.config import MAX_VIDEO_UPLOAD_SIZE

from django.http import HttpResponse

from utils import error, get_limits, extract_params

VIDEO_FIELDS_BASIC = ["description", "latitude", "longitude"]
VIDEO_FIELDS_OPTIONAL = ["altitude", "avaliable_to", "avaliable_from"]
VIDEO_FIELDS_COMPLETE = VIDEO_FIELDS_BASIC + ["owner", "video_data", "video_name"]

def video_upload (request, layer_id):
	format = getResponseFormat (request)
	if not request.user.is_authenticated():
		return error (format, "The user is not authenticated")
	try:
		if request.method == "POST":
			
			success, params = extract_params (request.POST, VIDEO_FIELDS_BASIC, VIDEO_FIELDS_OPTIONAL)
			
			if not success:
				return error (format, "Need mandatory POST param: %s" % (params))
			
			try:
				check_node_create(layer_id)
			except Layer_Does_Not_Exist, err:
				return error(format, err)
			except Layer_Perms, err:
				return error(format, err)
			
			params["owner"] = request.user.id
			form = VideoForm(request.POST, request.FILES)
			if form.is_valid():
				try:
					clean_data = form.cleaned_data
					params["video_data"] = clean_data['video']
					params["video_name"] = clean_data['name']
					params["uploader"] = request.user.pk
					
					if params["video_data"].size / 1000 > MAX_VIDEO_UPLOAD_SIZE:
						return error(format, "Video max size " + str(MAX_VIDEO_UPLOAD_SIZE) + "kb") 
					
					correct, message = api.video.upload (params) 
					
					if correct:
						video_id = message
						correct, message = api.node.set_privacy_default(video_id)
						if correct:
							correct, message = api.node.set_layer(video_id, layer_id)
							if correct:
								data = {'code'		 : '200',
									'id'		   : video_id,
									'description'  : 'Video created correctly',}
								return generateResponse(format, data, "ok")
							else:
								return error(format, message)
						else:
							return error(format, message) 
					else:
						return error(format, message)
				except:
					return error (format, sys.exc_value)
			else:
				return error (format, "Sent data not valid")
		else:
			return error (format, "Need a POST petition")
	except:
		return error (format, sys.exc_info())

