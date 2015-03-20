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
from django.contrib.gis.measure import D
from django.forms import DateField, ValidationError
from datetime import datetime 
import sys

from models import Person, Friendship, Photo
from utils import get_person, check_person_dict, get_fields_for_groups
from social.privacy.exceptions import PermissionError
from social.core.api_node import set_privacy_default

def create_or_modify(person, modify=True):
	"""
	Receives the Person data and adds it to the database, if the
	user is already created, modifies it
	"""
	
	from social.privacy2.models import Privacy
	try:
		person, message=check_person_dict(person)
		if person == None :
			return False, message
		p = None
		if "latitude" in person and "longitude" in person:
			try:
				point = Point(float(person["longitude"]), float(person["latitude"]), srid=4326)
			except:
				return False, "Bad latitude and/or longitude value/s"
		else:
			point = Point(0.0, 0.0, srid=4326)
		try:
			p = Person.objects.get(username=person["username"])
			if not modify:
				return False, "The user already exists"
			if not p.check_password(person["password"]):
				return False, "The password is incorrect"
			if "first_name" in person:
				p.first_name = person["first_name"]
			if "last_name" in person:
				p.last_name = person["last_name"]
			if "email" in person:
				p.email = person["email"]
			if "latitude" in person and "longitude" in person:
				p.position = point
				p.pos_time = datetime.now()
			if "altitude" in person:
				p.altitude = person["altitude"]
			if "ratius" in person:
				p.radius = person["radius"]
			if "birthday" in person:
				p.birthday = person["birthday"]
			if "country" in person:
				p.country = person["country"]
			if "post_code" in person:
				p.post_code = person["post_code"]
			if "new_password" in person:
				p.set_password(person["new_password"])
		except:
			if "birthday" in person and person["birthday"] is not None:
				field=DateField()
				try:
					person["birthday"]=field.clean(person["birthday"])
				except ValidationError:
					(type, value, trace)=sys.exc_info()
					try:
						return False, value.messages[0]
					except:
						return False, "Date format error"

			p = Person(username=person["username"],
					   first_name=person.setdefault("first_name",u""),
					   last_name=person.setdefault("last_name", u""),
					   password=person["password"],
					   email=person.setdefault("email", u""),
					   is_active=True,
					   position=point,
					   radius=float(person.setdefault("radius", u"0.0")),
					   birthday = person.setdefault("birthday", None),
					   country = person.setdefault("country", None),
					   post_code = person.setdefault("post_code", None),
					   altitude = person.setdefault("altitude", u"0.0"),
					   )

			p.set_password(person["password"])
			p.pos_time = datetime.now()

		p.save()
		return True, p.id
	except:
		return False, "Error Creating user"

def set_status(userid, status):
	"""
	Changes the user's status
	"""
	try:
		p = Person.objects.get(pk=userid)
		p.status = status
		p.status_time = datetime.now()
		p.save()
		return True, "No error"
	except:
		return False, "The user doesn't exist"
	
def set_avatar(userid, photoid):
	"""
	Changes the user's avatar
	"""
	try:
		try:
			p = Person.objects.get(pk=userid)
		except:
			return False, "The user doesn't exist"
		try:
			photo = Photo.objects.get(pk=photoid)
		except:
			return False, "The photo doesn't exist"
		if photo.uploader != p:
			return False, "This photo is not yours"
		p.avatar = photo
		p.save()
		return True, "No error"
	except:
		return False, "Unknown error occurred"

def get_friends(userid, viewer=None):
	"""
		Returns all friends for the user indicated
	"""
	try:
		v=get_person(viewer)
		p = Person.objects.get(pk=userid)
		if v:
			friends = Person.objects.allowed(v.id).distance(v.position).filter(
				  pk__in=Friendship.objects.get_relations_for(p)).order_by("distance")
			
		else:
			friends = Person.objects.distance(p.position).order_by("distance").filter(
				  pk__in=Friendship.objects.get_relations_for(p))
		
		return friends
	except:
		return []
	
def get_friendship_invitations(userid, viewer=None):
	"""
	Returns all the friendship invitations for the user 
	"""
	try:
		v=get_person(viewer)
		p = Person.objects.get(pk=userid)
		if v:
			friends = Person.objects.allowed(v.id).distance(v.position).order_by("distance").filter(
				  pk__in=Friendship.objects.get_invitations_for(p))
		else:
			friends = Person.objects.distance(p.position).order_by("distance").filter(
				  pk__in=Friendship.objects.get_invitations_for(p))  
		
		return friends
	except:
		return []

def get_nearby_friends(userid, radius, viewer=None):
	"""
	Finds friends in a radius (in km) from your position
	"""
	try:
		v=get_person(viewer)
		p = Person.objects.get(pk=userid)
		if v:
			friends = Person.objects.allowed(v.id).distance(v.position).order_by("distance").filter(
					position__distance_lte=(v.position, D(km=float(radius))),
					pk__in=Friendship.objects.get_relations_for(p))
		else:
			friends = Person.objects.distance(p.position).order_by("distance").filter(
					  position__distance_lte=(p.position, D(km=float(radius))),
					  pk__in=Friendship.objects.get_relations_for(p))
		
		return friends
	except:
		return []
		
def get_nearby_people(userid, radius, viewer=None):
	"""
	Finds people in a radius (in km) from your position
	"""
	try:
		v=get_person(viewer)
		p = Person.objects.get(pk=userid)
		if v:
			people = Person.objects.allowed(v.id).distance(v.position).order_by("distance").filter(position__distance_lte=(v.position, D(km=float(radius))))
		else:
			people = Person.objects.distance(p.position).order_by("distance").filter(position__distance_lte=(p.position, D(km=float(radius))))			
		
		return people
	except:
		return []

def delete(userid):
	"""
	 Deletes the person with this userid
	"""
	try:
		p = Person.objects.get(pk=userid)
		p.delete()
		return True, "No error"
	except:
		return False, "The user doesn't exist"

def create_friendship(person_id, friend_id):
	"""
	Creates a relation between the users whose names are indicated
	"""
	try:
		p1 = None
		p2 = None
		try:
			p1 = Person.objects.get(pk=person_id)
		except:
			return False, "Person id is incorrect"
		try:
			p2 = Person.objects.get(pk=friend_id)
		except:
			return False, "Friend id is incorrect"
		relation = None
		try:
			relation = Friendship.objects.get_relation(node1=p1, node2=p2)
		except:
			pass
		if relation==None:
			relation = Friendship(node1=p1, node2=p2)
		#Save more data...
		relation.save()
		return True, "No error"
	except:
		return False, "Unknown error"

def delete_friendship(person_id, friend_id):
	"""
	Deletes the relationship between the users
	"""
	try:
		p1 = None
		p2 = None
		try:
			p1 = Person.objects.get(pk=person_id)
		except:
			return False, "Person doesn't exist"
		try:
			p2 = Person.objects.get(pk=friend_id)
		except:
			return False, "Friend doesn't exist"
		Friendship.objects.delete_relation(node1=p1, node2=p2)
		return True, "No error"
	except:
		return False, "Unknown error"

def get_data(userid, viewer=None):
	"""
	Returns a dictionary with the user information
	"""
	try:
		p = Person.objects.get(pk=userid)
		v = get_person(viewer)
		return p.get_dictionary(viewer=v)
	except:
		return None

def get_all(viewer=None):
	
	try:
		v = get_person(viewer)
		if v:
			people = Person.objects.allowed(v.id).distance(v.position).order_by("distance")
		else:
			people = Person.objects.all()
		return people
	
	except:
		return []
