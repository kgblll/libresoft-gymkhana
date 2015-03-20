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
#	Author : Jose Antonio Santos Cadenas <jcaden __at__ gsyc __dot__ es>
#

from django.contrib.gis.geos import Point
#from django.contrib.gis.measure import D 

from models import Photo, Person
from utils import get_person, check_photo_dict, rand_name, get_correct_size, set_default_icon, get_visible_dates_interval
from social.core.custom_exceptions.social_core_exceptions import Social_Date_Exceptions
from social.core import config 

from PIL import Image

from social.privacy.exceptions import PermissionError

def upload (photo):
	"""
	Uploads a photo to the database accessible by a URL or PATH
	"""
	from social.privacy2.models import Privacy
	try:
		photo, message=check_photo_dict(photo)
		if photo == None :
			return False, message
		try:
			p = Person.objects.get(pk=photo["uploader"])
		except:
			return False, "The user doesn't exist"
		
		try:
			i = Image.open(photo["photo_data"])
			if not (i.format in config.SUPPORTED_TYPES):
				return False, "The image type is not supported"
		except IOError:
			return False, "The image is incorrect"

		try:
			point = Point(float(photo["longitude"]), float(photo["latitude"]), srid=4326)
		except:
			return False, "Bad latitude and/or longitude value/s"
		
		try:
			avaliable_from, avaliable_to = get_visible_dates_interval(photo)
			
			p = Photo(name=photo["photo_name"], uploader=p, position=point,
					  description=photo["description"], altitude=photo["altitude"], 
					  avaliable_from = avaliable_from, avaliable_to = avaliable_to)
	
			if p.icon is None or p.icon == "":
				set_default_icon(p)
			
			#photo name must be random because of security issue
			p.photo.save(rand_name(), photo["photo_data"])
			p.save()
	
			return True, p.id
		
		except Social_Date_Exceptions, msg:
			return False, msg
	except Exception, err:
		print err
		return False, "Error uploading photo"

def get_all (viewer=None):
	"""
	Shows all photos in the database
	"""
	try:
		v=get_person(viewer)
		#now = datetime.datetime.now()
		if v:
			photos_mod = Photo.objects.allowed(v.id).distance(v.position).order_by("distance")
		else:
			photos_mod = Photo.objects.all()
		
		return photos_mod
	except:
		return []

def get_data (photo_id, viewer=None):
	"""
	Returns an object with the photo data
	"""
	try:
		viewer=Person.objects.get(pk=viewer.id)
	except:
		viewer=None
	try:
		photo = Photo.objects.get(id=photo_id)
		p = photo.get_dictionary(viewer=viewer)
		return p
	except:
		return None

def get_image (photo_id, size=None, thumb=False, viewer=None):
	"""
	Returns the path to the image
	"""
	try:
		photo = Photo.objects.get(id=photo_id)
		try:
			viewer= Person.objects.get(pk=viewer.id)
		except:
			viewer=None
		path=photo.get_path(viewer=viewer)
		if path==None:
			return None
		if thumb:
			thumb_name = u"%s[thumb].jpeg" % path 
			try:
				img_thumb = Image.open(thumb_name)
			except:
				img_thumb = Image.open(path)
				w, h=img_thumb.size
				img_thumb.thumbnail (get_correct_size(100, 100, w, h))
				img_thumb.save(thumb_name)
			return thumb_name
		if size != None:
			max_w, max_h=size
			img =Image.open (path)
			w, h=img.size
			new_w, new_h = get_correct_size(max_w, max_h, w, h)
			if new_w>=w or new_h>=h:
				return path
			sized_img_name = u"%s[%sx%s].jpg" % (path, new_w, new_h) 
			try:
				Image.open(sized_img_name)
			except:
				img = img.resize((new_w, new_h))
				img.save(sized_img_name)
			return sized_img_name
		return path
	except:
		return None

def get_for_user (user_id, from_limit, to_limit, viewer=None):
	"""
	Shows all the user's photos
	"""
	try:
		total_elems = 0
		v=get_person(viewer)
		if v != None:
			photos_mod_all = Photo.objects.allowed(v.id).filter(uploader=user_id).distance(v.position).order_by("distance")
			photos_mod = photos_mod_all[from_limit:to_limit]
			total_elems = len (photos_mod_all)
		else:
			photos_mod = Photo.objects.filter(uploader=user_id)
			photos_mod = photos_mod_all[from_limit:to_limit]
			total_elems = len (photos_mod_all)
		photos = []
		for photo in photos_mod:
			try:
				p = photo.get_dictionary(v)
				photos += [p]
			except:
				pass
		return photos, total_elems
	except:
		return [], 0

def delete(photoid, user_id):
	"""
	@deprecated: use the node delete instead
	Deletes the photo indicated
	"""
	try:
		p = Photo.objects.get(pk=photoid)
		if p.uploader.id == user_id:
			p.delete()
		else:
			return False, "You can't delete this photo because, you are not the uploader"
		return True, "No error"
	except:
		return False, "This photo doesn't exist"
