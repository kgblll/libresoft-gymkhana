#
#  Copyright (C) 2009 GSyC/LibreSoft
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

from django.contrib.gis.geos import Point

from models import Sound, Person
from utils import get_person, check_sound_dict, rand_name, set_default_icon, get_visible_dates_interval
from social.core.custom_exceptions.social_core_exceptions import Social_Date_Exceptions
from social.core import config 

import sys

from social.privacy.exceptions import PermissionError

def upload (sound):
	"""
	Uploads a sound to the database accessible by a URL or PATH
	"""
	from social.privacy2.models import Privacy
	try:
		sound, message=check_sound_dict(sound)
		if sound == None :
			return False, message
		try:
			p = Person.objects.get(pk=sound["uploader"])
		except:
			return False, "The user doesn't exist"

# TODO check if the file is a sound file	   

		try:
			point = Point(float(sound["longitude"]), float(sound["latitude"]), srid=4326)
		except:
			return False, "Bad latitude and/or longitude value/s"
		
		try:
			avaliable_from, avaliable_to = get_visible_dates_interval(sound)
			
			s = Sound(name=sound["sound_name"], uploader=p, position=point,
					  description=sound["description"], altitude=sound["altitude"],  
					  avaliable_from = avaliable_from, avaliable_to = avaliable_to)
			
			if s.icon is None or s.icon == "":
				set_default_icon(s)
			
			s.sound.save(rand_name(), sound["sound_data"])
			s.save()
			return True, s.id
		
		except Social_Date_Exceptions, msg:
			return False, msg
		
		
	except:
		return False,  sys.exc_info()

def get_all (from_limit, to_limit, viewer=None):
	"""
	Shows all sounds in the database
	"""
	try:
		v=get_person(viewer)
		if v != None:
			sounds_mod = Sound.objects.allowed(v.id).distance(v.position).order_by("distance")[from_limit:to_limit]
		else:
			sounds_mod = Sound.objects.all()[from_limit:to_limit]
		sounds = []
		for sound in sounds_mod:
			try:
				s = sound.get_dictionary(v)
				sounds += [s]
			except PermissionError:
				pass
		return sounds
	except:
		return []

def get_data (sound_id, viewer=None):
	"""
	Returns an object with the sound data
	"""
	try:
		viewer=Person.objects.get(pk=viewer.id)
	except:
		viewer=None
	try:
		sound = Sound.objects.get(id=sound_id)
		s = sound.get_dictionary(viewer=viewer)
		return s
	except:
		return None

def get_sound_file (sound_id, viewer=None):
	"""
	Returns the path to the sound file
	"""
	try:
		photo = Sound.objects.get(id=sound_id)
		try:
			viewer= Person.objects.get(pk=viewer.id)
		except:
			viewer=None
		path=photo.get_path(viewer=viewer)
		return path
	except:
		return None

def get_for_user (user_id, from_limit, to_limit, viewer=None):
	"""
	Shows all the user's sounds
	"""
	try:
		total_elems = 0
		v=get_person(viewer)
		if v != None:
			sounds_mod_all = Sound.objects.allowed(v.id).filter(uploader=user_id).distance(v.position).order_by("distance")
			sounds_mod = sounds_mod_all[from_limit:to_limit]
			total_elems = len (sounds_mod_all)
		else:
			sounds_mod = Sound.objects.filter(uploader=user_id)
			sounds_mod = sounds_mod_all[from_limit:to_limit]
			total_elems = len (sounds_mod_all)
		sounds = []
		for sound in sounds_mod:
			try:
				s = sound.get_dictionary(v)
				sounds += [s]
			except:
				pass
		return sounds, total_elems
	except:
		return [],0

def delete(photoid, user_id):
	"""
	@deprecated: use the node delete instead
	Deletes the photo indicated
	"""
	try:
		s = Sound.objects.get(pk=photoid)
		if s.uploader.id == user_id:
			s.delete()
		else:
			return False, "You can't delete this sound because, you are not the uploader"
		return True, "No error"
	except:
		return False, "This sound doesn't exist"
