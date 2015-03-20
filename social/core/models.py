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

from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.core.files.storage import FileSystemStorage

from social.privacy2.utils import get_object_status, get_fields
import social.privacy2.utils as privacy

from datetime import datetime

from social.privacy.exceptions import PermissionError
from utils import get_fields_for_groups, get_group_for_field


	
class Tag(models.Model):
	"""
	Model for tag social objects
	"""
	tag = models.CharField(max_length=200, unique=True)
	
	objects = models.GeoManager()
	
	def get_search_fields(self):
		return ["tag"]
	
	def __unicode__(self):
		return u"%s" % self.tag
	
class Comment(models.Model):
	"""
	Allows comments on an object
	"""
	comment = models.TextField()
	
	date = models.DateTimeField(default=datetime.now(), editable=False)
	author = models.ForeignKey("Person", related_name="my_comments")
	node = models.ForeignKey("Social_node", related_name="comments")

	def get_dictionary(self):
		"""
		Returns a dictionary with the comment data
		"""
		dict = {"id"			  : self.id,
				"author" : { "id"	   : self.author.id,
							 "username" : self.author.username,
						   },
				"comment"		 : self.comment,
				"date"			: self.date
			   }
		return dict

class Social_node(models.Model):
	"""
	General social object, can be related with any other 
	social object
	"""
	position = models.PointField(srid=4326)
	altitude = models.FloatField(help_text="In meters over the sea level", default=0.0)
	radius = models.FloatField(default=0.0)
	pos_time = models.DateTimeField(default=datetime.now)
	since = models.DateTimeField(default=datetime.now)
	tags = models.ManyToManyField(Tag)
	type = models.CharField(max_length=50, editable=False)
	icon = models.CharField(max_length=200, null=True)
	avaliable_to = models.DateTimeField(null = True)
	avaliable_from = models.DateTimeField(null = True)
	# currently not used, maybe future features
	visible = models.BooleanField(default = True)
	
	info_url = models.CharField(max_length=200, null = True)
	
	objects = models.GeoManager()
	
	def save(self, force_insert=False, force_update=False):
		if not self.pk: #The first time
			m = ""
			for t in self._meta.get_parent_list():
				if t._meta.object_name.lower() != "social_node":
					if m == "":
						m = "%s" % (t._meta.object_name.lower())
					else:
						m = "%s.%s" % (m, t._meta.object_name.lower())
			if m == "":
				self.type = "%s" % self._meta.object_name.lower()
			else:	
				self.type = "%s.%s" % (m, self._meta.object_name.lower())
				
		"""
			There is a problem with the hierarchy of LGS Person (user.person). But, we dont have
			a user model, so this type could make problems. So, we have to forget the user class
		"""
		if self.type.find("user.") == 0:
			self.type = self.type.replace("user.", "") 
		return super(Social_node, self).save(force_insert, force_update)
	
	def get_type(self):
		try:
			if self.person.id == self.id:
				return "person"
		except:
			pass
		try:  
			if self.group.id == self.id:
				return "group"
		except:
			pass
		try:
			if self.note.id == self.id:
				return "note"
		except:
			pass
		try:
			if self.photo != None:
				return "photo"
		except:
			pass
		return "social_node"
	
	def get_node(self):
		try:
			node = eval("self.%s" % self.type)
			if isinstance(node, Social_node):
				try:
					node.distance = self.distance
				except:
					pass
				return node
		except:
			pass
		return self
	
	def get_owner(self):
		node = self.get_node()
		if node != self:
			return node.get_owner()
		else:
			return self
	
	def get_dictionary(self, viewer=None):
		"""
		Returns a dictionary with the node data
		"""
		dict = {"id"		: self.id,
				"position"  : {"latitude"  : self.position.get_y(),
							   "longitude" : self.position.get_x(),
							   "radius"	: self.radius,
							   "since"	 : self.pos_time,
							   "altitude"  : self.altitude,
							   },
				"since"	 : self.since,
				"type"	  : self.type,
				"tags"	  : [t.tag for t in self.tags.all()],
				"icon"	   : self.icon,
				"info_url" : self.info_url}
		try:
			dict["position"]["distance"]= round (self.distance.m,2)
		except:
			pass
		if viewer != None and viewer.id!=self.id:
			obj = self.get_node()
			groups= get_fields(obj, viewer)
			if groups==None:
				raise PermissionError("Element not allowed")
			fields= get_fields_for_groups(self, groups)
			if "id" not in fields:
				dict.pop("id")
			if "position" not in fields:
				pos=dict["position"]
				pos.pop("latitude")
				pos.pop("longitude")
				pos.pop("altitude")
				try:
					pos.pop("distance")
				except:
					pass
			if "radius" not in fields:
				dict["position"].pop("radius")
			if "pos_time" not in fields:
				dict["position"].pop("since")
			if dict["position"]=={}:
				dict.pop("position")
			if "since" not in fields:
				dict.pop("since")
		return dict

	def get_privacy(self):
		"""
		Returns a dictionary with the allowed and forbidden roles for each field
		"""
		object = self.get_node()
		sec = get_object_status(object)
		dict = self.get_dictionary()
		dict["allowed_all"]= sec["full"]
		dict["forbidden_all"]= sec["forbidden"]
		g=get_group_for_field(self, "id")
		
		dict["id"]={"value": dict["id"],
					"allowed": sec["fields_allowed"][g],
					"forbidden": sec["fields_forbidden"][g]}
		
		#self._get_location_privacy(dict)
		g=get_group_for_field(self, "position")
		dict["position"]["latitude"]={"value": dict["position"]["latitude"],
									  "allowed": sec["fields_allowed"][g],
									  "forbidden": sec["fields_forbidden"][g]}
		dict["position"]["longitude"]={"value": dict["position"]["longitude"],
									   "allowed": sec["fields_allowed"][g],
									   "forbidden": sec["fields_forbidden"][g]}
		dict["position"]["altitude"]={"value": dict["position"]["altitude"],
									   "allowed": sec["fields_allowed"][g],
									   "forbidden": sec["fields_forbidden"][g]}
		g=get_group_for_field(self, "radius")
		dict["position"]["radius"]={"value": dict["position"]["radius"],
									"allowed": sec["fields_allowed"][g],
									"forbidden": sec["fields_forbidden"][g]}
		g=get_group_for_field(self, "pos_time")
		dict["position"]["since"]={"value": dict["position"]["since"],
								   "allowed": sec["fields_allowed"][g],
								   "forbidden": sec["fields_forbidden"][g]}
	 
		g=get_group_for_field(self, "since")
		dict["since"]={"value": dict["since"],
					   "allowed": sec["fields_allowed"][g],
					   "forbidden": sec["fields_forbidden"][g]}
		return dict
	
	get_search_fields= []
	
	def set_perm(self, perm):
		return privacy.set_perm(self, perm)
	
	def set_perm_field(self, field, perm):
		return privacy.set_perm_field(self, field, perm)

	
	def delete(self, viewer):
		try:
			person = Person.objects.get(pk = viewer)
		except Exception, err:
			raise err
	
		super(Social_node, self).delete()


	@models.permalink
	def get_absolute_url(self):
		return ('node_data', [str(self.id)])
	
	def __unicode__(self):
		return u"social node %s" % self.pk

	
try: 
	from south.modelsinspector import add_introspection_rules
except ImportError: #ok, you dont have south in your system or you dont want to use it
	pass


class PersonManager(models.GeoManager):
	
	def allowed(self, viewer_id):
		return self.extra(where=[" social_node_ptr_id in (select * from get_persons_visibles(%s))" % viewer_id ])

class Person(Social_node, User):
	"""
	Represents a person in social networks issues
	"""
	status = models.CharField(max_length=500, default="")
	status_time = models.DateTimeField(default=datetime.now)
	birthday = models.DateField(null=True)
	post_code = models.CharField(max_length=15, null=True)
	country = models.CharField(max_length=2, null=True)
	avatar = models.ForeignKey("Photo", related_name="avatar_of", null=True)
	
	objects = PersonManager()

	def is_friend(self, friend):
		if Friendship.objects.are_friends(self, friend):
			return True
		else:
			return False
		
	def get_owner(self):
		return self

	def get_dictionary(self, viewer=None):
		"""
			Returns the person data as a dictionary
		"""
		dict = Social_node.get_dictionary(self, viewer)

		dict.setdefault("position", {})
		if self.country:
			dict['position']['country'] = self.country
		if self.post_code:
			dict['position']['post_code'] = self.post_code 
		dict['name']	 = self.get_full_name()
		dict['first_name'] = self.first_name
		dict['last_name']  = self.last_name
		dict['username'] = self.username
		dict['status']   = {"message":self.status,
							"since"  :self.status_time,
						   }
		dict['email']	= self.email
		if self.avatar:
			dict['avatar'] = {"id"  : self.avatar.id,
							  "url" : self.avatar.get_absolute_image_url()}
		if self.birthday:
			dict['birthday'] = self.birthday
			
		if viewer !=None and viewer!=self:
			groups = get_fields(self, viewer)
			if groups==None:
				raise PermissionError("Element not allowed")
			fields= get_fields_for_groups(self, groups)
			if "name" not in fields:
				dict.pop("name")
			if "first_name" not in fields:
				dict.pop("first_name")
			if "last_name" not in fields:
				dict.pop("last_name")
			if "username" not in fields:
				dict.pop("username")
			if "status" not in fields:
				dict["status"].pop("message")
			if "status_time" not in fields:
				dict["status"].pop("since")
			if dict["status"]=={}:
				dict.pop("status")
			if "email" not in fields:
				dict.pop("email")
			if "birthday" not in fields and self.birthday:
				dict.pop("birthday")
			if "country" not in fields and self.country:
				dict["position"].pop("country")
			if "post_code" not in fields and self.post_code:
				dict["position"].pop("post_code")
			if dict["position"]=={}:
				dict.pop("position")
			if "avatar" not in fields and self.avatar:
				dict.pot("avatar")
		return dict
	
	get_search_fields=Social_node.get_search_fields + \
					  ["first_name", "last_name", "username", "status", "email"]
	
	def get_privacy(self):
		"""
		Returns a dictionary with the allowed and forbidden roles for each field
		"""
		sec = get_object_status(self)
		dict_1 = self.get_dictionary()
		dict = Social_node.get_privacy(self)
		dict["allowed_all"] = list(set(sec["full"]+dict["allowed_all"]))
		dict["forbidden_all"] = list(set(sec["forbidden"]+dict["forbidden_all"]))
		
		g=get_group_for_field(self, "first_name")
		dict["name"]={"value": dict_1["name"],
					  "allowed": sec["fields_allowed"][g],
					  "forbidden": sec["fields_forbidden"][g]}
		g=get_group_for_field(self, "username")
		dict["username"]={"value": dict_1["username"],
						  "allowed": sec["fields_allowed"][g],
						  "forbidden": sec["fields_forbidden"][g]}
		g=get_group_for_field(self, "status")
		dict["status"]["message"]={"value": dict_1["status"]["message"],
								   "allowed": sec["fields_allowed"][g],
								   "forbidden": sec["fields_forbidden"][g]}
		g=get_group_for_field(self, "status_time")
		dict["status"]["since"]={"value": dict_1["status"]["since"],
								 "allowed": sec["fields_allowed"][g],
								 "forbidden": sec["fields_forbidden"][g]}
		g=get_group_for_field(self, "email")
		dict["email"]={"value": dict_1["email"],
					   "allowed": sec["fields_allowed"][g],
					   "forbidden": sec["fields_forbidden"][g]}
		g=get_group_for_field(self, "birthday")
		dict["birthday"]={"value": dict_1["position"].setdefault("birthday", None),
					   "allowed": sec["fields_allowed"][g],
					   "forbidden": sec["fields_forbidden"][g]}
		g=get_group_for_field(self, "country")
		dict["position"]["country"]={"value": dict_1["position"].setdefault("country", None),
									 "allowed": sec["fields_allowed"][g],
									 "forbidden": sec["fields_forbidden"][g]}
		g=get_group_for_field(self, "country")
		dict["position"]["post_code"]={"value": dict_1["position"].setdefault("post_code", None),
									   "allowed": sec["fields_allowed"][g],
									   "forbidden": sec["fields_forbidden"][g]}
		g=get_group_for_field(self, "avatar")
		dict["avatar"]={"avatar": dict_1.setdefault("avatar", None),
						"allowed": sec["fields_allowed"][g],
						"forbidden": sec["fields_forbidden"][g]}
		return dict
	
	"""
	Functions to return information the system needs making backups with binaries included
	In the case of person, this social node does not include binary information
	"""
	
	def get_binary_path(self, viewer = None):
		return None
	
	def get_binary_attr_name(self):
		return None
	
	@models.permalink
	def get_absolute_url(self):
		return ('person_data', [str(self.id)])

	def __unicode__(self):
		return self.username

class Group(Social_node):
	"""
	A group of people
	"""
	name = models.CharField(max_length=200, unique=True)
	
	objects = models.GeoManager()
	
	def get_dictionary(self, viewer=None):
		"""
		Returns the group data as a dictionary
		"""
		dict = Social_node.get_dictionary(self, viewer)
		dict["groupname"]=self.name
		if viewer!=None:
			fields = get_fields(self, viewer)
			groups = get_fields(self, viewer)
			if groups==None:
				raise PermissionError("Element not allowed")
			fields= get_fields_for_groups(self, groups)
			if "groupname" not in fields:
				dict.pop("groupname")
		return dict
	
	get_search_fields=Social_node.get_search_fields + ["name"] 
	

	@models.permalink
	def get_absolute_url(self):
		return ('group_data', [str(self.id)])
	
	def __unicode__(self):
		return self.name
	
	class Meta:
		verbose_name = "group"

	"""
	Functions to return information the system needs making backups with binaries included
	In the case of group, this social node does not include binary information
	"""
	
	def get_binary_path(self, viewer = None):
		return None
	
	def get_binary_attr_name(self):
		return None
	
class NoteManager(models.GeoManager):
	
	def allowed(self, viewer_id):
		return self.extra(where=["id in (select * from get_notes_visibles(%s))" % viewer_id ])

class Note(Social_node):
	"""
	   A note 
	"""
	title = models.CharField(max_length=200)
	text = models.TextField()
	uploader = models.ForeignKey(Person)

	objects = NoteManager()
	
	def get_owner(self):
		return self.uploader
	
	def get_dictionary(self, viewer=None):
		"""
			Returns the note data as a dictionary
		"""
		allow= (viewer == None) or viewer == self.uploader
		if allow:
			dict = Social_node.get_dictionary(self, None)
		else:
			dict = Social_node.get_dictionary(self, viewer)
		dict["title"]=self.title
		dict["text"]=self.text
		try:
			"""
			Only returns the basic user info, more information using the user api
			with the privacy restrictions
			"""			 
			uploader_dict = self.uploader.get_dictionary(viewer)
			dict["uploader"] = {"id" : uploader_dict["id"],
							   "username" : uploader_dict["username"],
							   "type": uploader_dict["type"]}
		except PermissionError:
			pass
		
		if not allow:
			groups = get_fields(self, viewer)
			if groups==None:
				raise PermissionError("Element not allowed")
			fields= get_fields_for_groups(self, groups)
			if "title" not in fields:
				dict.pop("title")
			if "text" not in fields:
				dict.pop("text")
			if "uploader" not in fields:
				try:
					dict.pop("uploader")
				except:
					pass
		return dict
	
	def get_privacy(self):
		"""
		Returns a dictionary with the allowed and forbidden roles for each field
		"""
		sec = get_object_status(self)
		dict_1 = self.get_dictionary()
		dict = Social_node.get_privacy(self)
		dict["allowed_all"] = list(set(sec["full"]+dict["allowed_all"]))
		dict["forbidden_all"] = list(set(sec["forbidden"]+dict["forbidden_all"]))
		
		g=get_group_for_field(self, "title")
		dict["title"]={"value": dict_1["title"],
					   "allowed": sec["fields_allowed"][g],
					   "forbidden": sec["fields_forbidden"][g]}
		g=get_group_for_field(self, "text")
		dict["text"]={"value": dict_1["text"],
					  "allowed": sec["fields_allowed"][g],
					  "forbidden": sec["fields_forbidden"][g]}
		g=get_group_for_field(self, "uploader")
		dict["uploader"]={"value": dict_1["uploader"]["id"],
					  "allowed": sec["fields_allowed"][g],
					  "forbidden": sec["fields_forbidden"][g]}
		
		return dict
	
	get_search_fields=Social_node.get_search_fields + ["title", "text"]
	
	@models.permalink
	def get_absolute_url(self):
		return ('note_data', [str(self.id)])
	
	def __unicode__(self):
		return self.title	

	"""
	Functions to return information the system needs making backups with binaries included
	In the case of note, this social node does not include binary information
	"""
	
	def get_binary_path(self, viewer = None):
		return None
	
	def get_binary_attr_name(self):
		return None
	
	
class SoundManager(models.GeoManager):
	
	def allowed(self, viewer_id):
		return self.extra(where=["id in (select * from get_sounds_visibles(%s))" % viewer_id ])

class Sound(Social_node):
	"""
	A sound file
	"""
	name = models.CharField(max_length=200)
	sound = models.FileField(upload_to="sounds/", blank=False,
							  null=False, max_length=200, 
							  storage=FileSystemStorage())
	description = models.TextField()
	uploader = models.ForeignKey(Person)
	sound_url = models.CharField(max_length=200, null = True)
	get_search_fields=Social_node.get_search_fields + ["name", "description"]

	@models.permalink
	def get_absolute_url(self):
		return ('node_data', [str(self.uploader.id), str(self.id)])
	
	@models.permalink
	def get_absolute_image_url(self):
		return ('node_sound_file', [str(self.uploader.id), str(self.id)])

	def get_path(self, viewer=None):
		if viewer!=None and self.uploader!=viewer:
			groups = get_fields(self, viewer)
			if groups==None:
				return None
			fields= get_fields_for_groups(self, groups)
			if "sound" not in fields:
				return None
		return self.sound.path

	objects = SoundManager()
	
	def get_owner(self):
		return self.uploader
	
	def get_dictionary(self, viewer=None):
		"""
		Returns the note data as a dictionary
		"""
		allow = viewer==None or self.uploader==viewer
		if allow:
			dict = Social_node.get_dictionary(self, None)
		else:
			dict = Social_node.get_dictionary(self, viewer)
		
		dict["name"]=self.name
		dict["description"]=self.description
		try:
			"""
			Only returns the basic user info, more information using the user api
			with the privacy restrictions
			"""			 
			uploader_dict = self.uploader.get_dictionary(viewer)
			dict["uploader"] = {"id" : uploader_dict["id"],
							   "username" : uploader_dict["username"],
							   "type": uploader_dict["type"]}
		except PermissionError:
			pass
		#dict["url"]=self.get_absolute_url()
		#dict["image_url"]=self.get_absolute_image_url()
		
		if not allow:
			groups = get_fields(self, viewer)
			if groups==None:
				raise PermissionError("Element not allowed")
			fields= get_fields_for_groups(self, groups)
			if "name" not in fields:
				dict.pop("name")
			if "description" not in fields:
				dict.pop("description")
			if "uploader" not in fields:
				try:
					dict.pop("uploader")
				except:
					pass
		return dict
	
	def get_privacy(self):
		"""
		Returns a dictionary with the allowed and forbidden roles for each field
		"""
		sec = get_object_status(self)
		dict_1 = self.get_dictionary()
		dict = Social_node.get_privacy(self)
		dict["allowed_all"] = list(set(sec["full"]+dict["allowed_all"]))
		dict["forbidden_all"] = list(set(sec["forbidden"]+dict["forbidden_all"]))
		
		g=get_group_for_field(self, "name")
		dict["name"]={"value": dict_1["name"],
					  "allowed": sec["fields_allowed"][g],
					  "forbidden": sec["fields_forbidden"][g]}
		g=get_group_for_field(self, "description")
		dict["description"]={"value": dict_1["description"],
							 "allowed": sec["fields_allowed"][g],
							 "forbidden": sec["fields_forbidden"][g]}
		g=get_group_for_field(self, "uploader")
		dict["uploader"]={"value": dict_1["uploader"]["id"],
						  "allowed": sec["fields_allowed"][g],
						  "forbidden": sec["fields_forbidden"][g]}
		return dict
	
	def __unicode__(self):
		return self.name

	"""
	Functions to return information the system needs making backups with binaries included
	"""
	
	def get_binary_path(self, viewer = None):
		return self.get_path(viewer)
	
	def get_binary_attr_name(self):
		return "sound_url"
	
class PhotoManager(models.GeoManager):
	
	def allowed(self, viewer_id):
		return self.extra(where=["id in (select * from get_photos_visibles(%s))" % viewer_id ])

class Photo(Social_node):
	"""
	A photo
	"""
	name = models.CharField(max_length=200)
	photo = models.ImageField(upload_to="images/photos/", blank=False,
							  null=False, max_length=200, 
							  storage=FileSystemStorage())
	description = models.TextField()
	uploader = models.ForeignKey(Person)
	
	photo_url = models.CharField(max_length=200, null = True)
	photo_medium_url = models.CharField(max_length=200, null = True)
	photo_thumb_url = models.CharField(max_length=200, null = True)
	

	get_search_fields=Social_node.get_search_fields + ["name", "description"]

	@models.permalink
	def get_absolute_url(self):
		return ('node_data', [str(self.uploader.id), str(self.id)])
	
	@models.permalink
	def get_absolute_image_url(self):
		return ('node_image', [str(self.uploader.id) , str(self.id)])

	def get_path(self, viewer=None):
		return self.photo.path
		if viewer!=None and self.uploader!=viewer:
			groups = get_fields(self, viewer)
			if groups==None:
				return None
			fields= get_fields_for_groups(self, groups)
			if "photo" not in fields:
				return None
		return self.photo.path

	objects = PhotoManager()
	
	def get_owner(self):
		return self.uploader
	
	def get_dictionary(self, viewer=None):
		"""
		Returns the note data as a dictionary
		"""
		allow = viewer==None #or self.uploader==viewer
		if allow:
			dict = Social_node.get_dictionary(self, None)
		else:
			dict = Social_node.get_dictionary(self, viewer)
		
		dict["name"] = self.name
		dict["description"] = self.description
		dict["photo_url"] = self.photo_url
		dict["photo_medium_url"] = self.photo_medium_url
		dict["photo_thumb_url"] = self.photo_thumb_url
				
		try:
			"""
			Only returns the basic user info, more information using the user api
			with the privacy restrictions
			"""			 
			uploader_dict = self.uploader.get_dictionary(viewer)
			dict["uploader"] = {"id" : uploader_dict["id"],
							   "username" : uploader_dict["username"],
							   "type": uploader_dict["type"]}
		except PermissionError:
			pass
		#dict["url"]=self.get_absolute_url()
		#dict["image_url"]=self.get_absolute_image_url()
		
		if not allow:
			groups = get_fields(self, viewer)
			if groups==None:
				raise PermissionError("Element not allowed")
			fields= get_fields_for_groups(self, groups)
			if "name" not in fields:
				dict.pop("name")
			if "description" not in fields:
				dict.pop("description")
			if "uploader" not in fields:
				try:
					dict.pop("uploader")
				except:
					pass
		return dict
	
	def get_privacy(self):
		"""
		Returns a dictionary with the allowed and forbidden roles for each field
		"""
		sec = get_object_status(self)
		dict_1 = self.get_dictionary()
		dict = Social_node.get_privacy(self)
		dict["allowed_all"] = list(set(sec["full"]+dict["allowed_all"]))
		dict["forbidden_all"] = list(set(sec["forbidden"]+dict["forbidden_all"]))
		
		g=get_group_for_field(self, "name")
		dict["name"]={"value": dict_1["name"],
					  "allowed": sec["fields_allowed"][g],
					  "forbidden": sec["fields_forbidden"][g]}
		g=get_group_for_field(self, "description")
		dict["description"]={"value": dict_1["description"],
							 "allowed": sec["fields_allowed"][g],
							 "forbidden": sec["fields_forbidden"][g]}
		g=get_group_for_field(self, "uploader")
		dict["uploader"]={"value": dict_1["uploader"]["id"],
						  "allowed": sec["fields_allowed"][g],
						  "forbidden": sec["fields_forbidden"][g]}
		return dict
	
	def delete(self, viewer):
			
		try:
			person = Person.objects.get(pk = viewer)
		except Exception, err:
			raise err

		if person.avatar != None and self.id == person.avatar.id:
			person.avatar = None
			person.save()
		
		super(Photo, self).delete(viewer)

	def __unicode__(self):
		return self.name

	"""
	Functions to return information the system needs making backups with binaries included
	"""
	
	def get_binary_path(self, viewer = None):
		return self.get_path(viewer)
	
	def get_binary_attr_name(self):
		return "photo_url"
	
class VideoManager(models.GeoManager):
	
	def allowed(self, viewer_id):
		return self.extra(where=["id in (select * from get_videos_visibles(%s))" % viewer_id ])

class Video(Social_node):
	"""
	   A video node 
	"""
	name = models.CharField(max_length=200)
	description = models.TextField()
	video = models.FileField (upload_to="videos/", blank=False,
							  null=False, max_length=200, 
							  storage=FileSystemStorage())
	uploader = models.ForeignKey(Person)
	video_url = models.CharField(max_length=200, null = True)
	video_thumb_url = models.CharField(max_length=200, null = True)
	

	objects = VideoManager()
	
	def get_owner(self):
		return self.uploader
	
	def get_dictionary(self, viewer=None):
		"""
			Returns the note data as a dictionary
		"""
		allow= (viewer == None) or viewer == self.uploader
		if allow:
			dict = Social_node.get_dictionary(self, None)
		else:
			dict = Social_node.get_dictionary(self, viewer)
			
		dict["name"] = self.name
		dict["description"] = self.description
		dict["video_url"] = self.video_url
		dict["video_thumb_url"] = self.video_thumb_url
		
				
		try:
			"""
			Only returns the basic user info, more information using the user api
			with the privacy restrictions
			"""			 
			uploader_dict = self.uploader.get_dictionary(viewer)
			dict["uploader"] = {"id" : uploader_dict["id"],
							   "username" : uploader_dict["username"],
							   "type": uploader_dict["type"]}
		except PermissionError:
			pass
		
		
		if not allow:
			groups = get_fields(self, viewer)
			if groups==None:
				raise PermissionError("Element not allowed")
			fields= get_fields_for_groups(self, groups)
			if "name" not in fields:
				dict.pop("name")
			if "description" not in fields:
				dict.pop("description")
			if "uploader" not in fields:
				try:
					dict.pop("uploader")
				except:
					pass
		return dict
	
	def get_privacy(self):
		"""
		Returns a dictionary with the allowed and forbidden roles for each field
		"""
		sec = get_object_status(self)
		dict_1 = self.get_dictionary()
		dict = Social_node.get_privacy(self)
		dict["allowed_all"] = list(set(sec["full"]+dict["allowed_all"]))
		dict["forbidden_all"] = list(set(sec["forbidden"]+dict["forbidden_all"]))
		
		g=get_group_for_field(self, "name")
		dict["name"]={"value": dict_1["name"],
					   "allowed": sec["fields_allowed"][g],
					   "forbidden": sec["fields_forbidden"][g]}
		g=get_group_for_field(self, "description")
		dict["description"]={"value": dict_1["description"],
					  "allowed": sec["fields_allowed"][g],
					  "forbidden": sec["fields_forbidden"][g]}
		g=get_group_for_field(self, "uploader")
		dict["uploader"]={"value": dict_1["uploader"]["id"],
					  "allowed": sec["fields_allowed"][g],
					  "forbidden": sec["fields_forbidden"][g]}
		
		return dict
	
	get_search_fields=Social_node.get_search_fields + ["name", "description"]
	
	@models.permalink
	def get_absolute_url(self):
		return ('video_data', [str(self.id)])
	
	def get_path(self, viewer=None):

		if viewer!=None and self.uploader!=viewer:
			groups = get_fields(self, viewer)
			if groups==None:
				return None
			fields = get_fields_for_groups(self, groups)
			if "video" not in fields:
				return None
		return self.video.path
	
	def __unicode__(self):
		return self.name	

	"""
	Functions to return information the system needs making backups with binaries included
	"""
	
	def get_binary_path(self, viewer = None):
		return self.get_path(viewer)
	
	def get_binary_attr_name(self):
		return "video_url"

class LayerManager(models.GeoManager):
	
	def allowed(self, viewer_id):
		return self.extra(where=["id in (select * from get_layers_visibles(%s))" % viewer_id ])

	
class Layer(Social_node):
	"""
	   A layer 
	"""
	
	LAYER_TYPE = (
					('OF', 'Official'),
					('USR', 'USER')
				 )
	objects = LayerManager()
	
	name = models.CharField(max_length=200)
	description = models.TextField()
	layer_type = models.CharField(max_length = 10, choices = LAYER_TYPE)
	writeable = models.BooleanField(null=False) 
	free = models.BooleanField(null=False)
	external = models.BooleanField(null=False) 
	default = models.BooleanField(null=False, default=False)
	uploader = models.ForeignKey(Person)
		
	def get_owner(self):
		return self.uploader
	
	def get_dictionary(self, viewer=None):
		"""
			Returns the layer data as a dictionary
		"""
		allow= (viewer == None) or viewer == self.uploader
		if allow:
			dict = Social_node.get_dictionary(self, None)
		else:
			dict = Social_node.get_dictionary(self, viewer)

		dict["id"] = self.id
		dict["type"] = self.type
		dict["name"] = self.name
		dict["description"] = self.description
		dict["free"] = self.free
		dict["writeable"] = self.writeable
		dict["layer_type"] = self.layer_type
		dict["external"] = self.external
		
		try:
			"""
			Only returns the basic user info, more information using the user api
			with the privacy restrictions
			"""			 
			uploader_dict = self.uploader.get_dictionary(viewer)
			dict["uploader"] = {"id" : uploader_dict["id"],
							   "username" : uploader_dict["username"],
							   "type": uploader_dict["type"]}
			
		except PermissionError:
			print PermissionError
			pass
		
		if not allow:
			groups = get_fields(self, viewer)
			if groups==None:
				raise PermissionError("Element not allowed")
			fields= get_fields_for_groups(self, groups)
			if "name" not in fields:
				dict.pop("name")
			if "description" not in fields:
				dict.pop("description")
			if "uploader" not in fields:
				try:
					dict.pop("uploader")
				except:
					pass

		return dict
	
	def get_privacy(self):
		"""
		Returns a dictionary with the allowed and forbidden roles for each field
		"""

		sec = get_object_status(self)
		dict_1 = self.get_dictionary()
		dict = Social_node.get_privacy(self)
		dict["allowed_all"] = list(set(sec["full"]+dict["allowed_all"]))
		dict["forbidden_all"] = list(set(sec["forbidden"]+dict["forbidden_all"]))
		
		g=get_group_for_field(self, "name")
		dict["name"]={"value": dict_1["name"],
					  "allowed": sec["fields_allowed"][g],
					  "forbidden": sec["fields_forbidden"][g]}
		g=get_group_for_field(self, "description")
		dict["description"]={"value": dict_1["description"],
							 "allowed": sec["fields_allowed"][g],
							 "forbidden": sec["fields_forbidden"][g]}
		g=get_group_for_field(self, "position")
		dict["position"]={"value": dict_1["position"],
							 "allowed": sec["fields_allowed"][g],
							 "forbidden": sec["fields_forbidden"][g]}
		g=get_group_for_field(self, "uploader")
		dict["uploader"]={"value": dict_1["uploader"]["id"],
						  "allowed": sec["fields_allowed"][g],
						  "forbidden": sec["fields_forbidden"][g]}
		return dict
	
	def set_node(self, node_id):
		relations = LayerNodes.objects.get_relation(node1 = self.id, node2 = node_id)
		
		if relations == None:
			node = Social_node.objects.get(id = node_id)
			relation, created = LayerNodes.objects.get_or_create(node1 = self, node2 = node)
		
			if created:
				return True, relation
			else:
				return False, "Error node exists in the layer"
		else:
			return False, "Error: node is included in the layer"
			

	@models.permalink
	def get_absolute_url(self):
		return ('layer_data', [str(self.id)])
	
	def __unicode__(self):
		return self.name	

	"""
	Functions to return information the system needs making backups with binaries included
	"""
	
	def get_binary_path(self, viewer = None):
		return None
	
	def get_binary_attr_name(self):
		return None
	

class RelationManager(models.GeoManager):  
	def get_relation(self, node1, node2):
		try:
			relation = self.get(node1=node1, node2=node2)
			return relation
		except:
			try:
				relation = self.get(node1=node2, node2=node1)
				return relation
			except:
				return None
		return None
	
	def get_relations_for (self, node):
		relations=[n for n in self.values_list("node1", flat=True).filter(node2=node)]
		relations+=[n for n in self.values_list("node2", flat=True).filter(node1=node).exclude(node2__pk__in=relations)]
		return relations

class Relation(models.Model):
	"""
	Represents the relation between two social_nodes
	"""
	node1 = models.ForeignKey(Social_node, related_name="related")
	node2 = models.ForeignKey(Social_node, related_name="__related")
	since = models.DateTimeField(default=datetime.now)
	
	objects = RelationManager()
	
	def __unicode__(self):
		return u"%s <--> %s" % (self.node1, self.node2)
	
class FriendshipManager(RelationManager):
	"""
	This is the friendship manager, friendship relation is special because must be bidirectional,
	if the relation only appears in one direction, is not a friendship, is a friendship request 
	"""
	def delete_relation(self, node1, node2):
		relation = self.get_relation(node1, node2)
		if relation != None:
			relation.delete()
		relation2 = self.get_relation(node2, node1)
		if relation2 != None:
			relation2.delete()
	
	def get_relation(self, node1, node2):
		try:
			relation = self.get(node1=node1, node2=node2)
			return relation
		except:
			return None
	
	def get_relations_for (self, node):
		relations=self.values_list("node1", flat=True).filter(node2=node)
		friends=[]
		for n in relations:
			try:
				self.get(node2=n, node1=node)
				#No exception means that there is an object, so they are friends
				friends.append(n)
			except:
				pass
		return friends
	
	def get_relation_invitation(self, node1, node2):
		"""
		Returns a tuple with two relation objects, the friendship first and
		the friendship invitation second.
		
		@param node1: the fist person id or object
		@param node2: the second person id or object
		
		@return: A tuple with two Friendship objects (friendship, invitation) 
		"""
		try:
			relation1 = self.get(node1=node1, node2=node2)
			relation2 = self.get(node1=node2, node2=node1)
			if relation1.since< relation2.since:
				#The older is the invitation, so goes the second
				return (relation2, relation1)
			else:
				return (relation1, relation2)
				pass
		except:
			return None
	
	def get_invitations_for (self, node):
		"""
		Returns an array with the id's of all the non accepted invitations
		
		@param node: The id or object
		
		@return: An array with the users ids that requested a friendship
		"""
		relations=self.values_list("node1", flat=True).filter(node2=node)
		invitations=[]
		for n in relations:
			try:
				self.get(node2=n, node1=node)
				#No exception means that there is an object, so they are friends
			except:
				invitations.append(n)
		return invitations
	
	def are_friends_of_friends(self, user1, user2):
		if self.are_friends(user1, user2):
			return True
		friends = self.get_relations_for(user1)
		for f in friends:
			if self.are_friends(f, user2):
				return True 
		return False
	
	def are_friends(self, user1, user2):
		"""
		Returns true or false if user1 and user2 are friends or not
		
		@param user1: A user
		@param user2: Another user
		
		@return: Boolean, True if they are friends False otherwise.
		"""
		rel1=self.get_relation(user1, user2)
		if rel1==None:
			return False
		rel2=self.get_relation(user2, user1)
		if rel2==None:
			return False
		return True
	
	def get_friends(self):
		raise NotImplementedError( "Sorry this method is not implemented yet" )

class Friendship(Relation):
	"""
	Specific relation between persons 
	"""
	objects = FriendshipManager()
	
class LayerNodesManager(RelationManager):
	
	def get_pass(self):
		pass
	
	def get_layers_for_node(self, social_node):
		relations = self.values_list("node1", flat=True).filter(node2 = social_node)
		return relations
		
	def get_nodes_for_layer(self, layer):
		relations = self.values_list("node2", flat=True).filter(node1 = layer)
		return relations
	
class LayerNodes(Relation):
	
	objects = LayerNodesManager()
	
	def get_dictionary(self, viewer=None):
		"""
			Returns the relation between layers an nodes
		"""
		dict["id_layer"] = self.node1
		dict["id_node"] = self.node2
		dict["since"] = self.since
		
		return dict
class MembershipManager(RelationManager):
	
	def get_groups_for(self, user):
		"""
		Returns the groups for the user
		
		@param user: The user object
		
		@Return a Queryset with all the groups
		"""
		
		return Group.objects.filter(id__in=self.filter(node1=user).values_list("node2", flat=True))
	
class Membership(Relation):
	"""
	Specific relation between persons and groups.
		
	Node1 must be the person and node2 the group
	"""
	
	def save(self, force_insert=False, force_update=False):
		is_group = False
		try:  
			if self.node2.group.id == self.node2.id:
				is_group = True
		except:
			pass
		if not is_group:
			raise ValueError("Membership node2 must be a group.")
		
		if force_insert and force_update:
			raise ValueError("Cannot force both insert and updating in "
					"model saving.")
		self.save_base(force_insert=force_insert, force_update=force_update)
	
	objects = MembershipManager()
