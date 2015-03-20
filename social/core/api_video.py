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
#	Author :  Jose Gato Luis <jgato@libresoft.es>
#
 
from django.contrib.gis.geos import Point

from models import Video, Person
from utils import check_video_dict, check_video_supported, rand_name, set_default_icon, get_visible_dates_interval
from social.core.custom_exceptions.social_core_exceptions import Social_Date_Exceptions


import sys


from social.core.custom_exceptions.social_core_exceptions import VIDEO_NOT_SUPPORTED

def upload (video):
	"""
	Uploads a video to the database accessible by a URL or PATH
	"""
	from social.privacy2.models import Privacy
	try:
		
		if not check_video_supported(video):
			raise VIDEO_NOT_SUPPORTED
		
		video, message = check_video_dict(video)
		
		if video == None :
			return False, message
		try:
			p = Person.objects.get(pk=video["uploader"])
		except:
			return False, "The user doesn't exist"

		
		try:
			point = Point(float(video["longitude"]), float(video["latitude"]), srid=4326)
		except:
			return False, "Bad latitude and/or longitude value/s"
		
		try:
			avaliable_from, avaliable_to = get_visible_dates_interval(video)
			
			video_node = Video( name = video["video_name"], uploader = p, position = point,
					  description = video["description"], altitude = video["altitude"],  
					  avaliable_from = avaliable_from, avaliable_to = avaliable_to)
			
			if video_node.icon is None or video_node.icon == "":
				set_default_icon(video_node)
			
			print video_node
			
			video_node.video.save(rand_name(), video["video_data"])
			video_node.save()
			
			return True, video_node.id
		
		except Social_Date_Exceptions, msg:
			return False, msg
		
		
	except:
		return False,  sys.exc_info()


def get_video_file (video_id, viewer=None):
	"""
	Returns the path to the video file
	"""
	try:
		video = Video.objects.get(id = video_id)
		try:
			viewer = Person.objects.get(pk = viewer.id)
		except:
			viewer = None
		path = video.get_path( viewer = viewer)
		return path
	except:
		return None

