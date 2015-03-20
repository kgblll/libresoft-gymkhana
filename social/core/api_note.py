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
from django.core.exceptions import MultipleObjectsReturned

from models import Note, Person
from utils import get_person, check_note_dict, set_default_icon, get_visible_dates_interval
from social.privacy.exceptions import PermissionError
from social.core.custom_exceptions.social_core_exceptions import Social_Date_Exceptions
from social.core import config 

def create(note):
	"""
	Creates a new note
	"""
	from social.privacy2.models import Privacy
	try:
		note, message=check_note_dict(note)
		if note == None :
			return False, message
		point = Point(float(note["longitude"]), float(note["latitude"]), srid=4326)
		try:
			p = Person.objects.get(pk=note["owner"])
		except:
			return False, "Not valid uploader"
		
		try:
			avaliable_from, avaliable_to = get_visible_dates_interval(note)
			
			note = Note(title=note["title"], text=note["text"], position=point, uploader = p,
						altitude=note["altitude"], 
						avaliable_from = avaliable_from, avaliable_to = avaliable_to);
			
			if note.icon is None or note.icon == "":
				set_default_icon(note)
			note.save()

			return True, note.id
		
		except Social_Date_Exceptions, msg:
			return False, msg
		except:
			return False, "Note can't be created"
	except:
		return False, "Unknown error"

def get_all(from_limit, to_limit, viewer=None):
	"""
	Returns an array with all the Notes
	"""
	try:
		v=get_person(viewer)
		if v != None:
			notes_mod = Note.objects.allowed(v.id).distance(v.position).order_by("distance")[from_limit:to_limit]
		else:
			notes_mod = Note.objects.all()[from_limit:to_limit]
		notes = []
		for note in notes_mod:
			try:
				n = note.get_dictionary(viewer=v)
				notes += [n]
			except PermissionError:
				pass
		return notes
	except:
		return []
	
def get_data(note_id, viewer=None):
	"""
	Returns the details for a note
	"""
	try:
		v = get_person(viewer)
		n = Note.objects.get(id=note_id)
		note = n.get_dictionary(viewer=v)
		return note
	except:
		return None

def get_for_user(user_id, from_limit, to_limit, viewer=None):
	"""
	Returns all the user's notes
	"""
	try:
		total_elems = 0
		v=get_person(viewer)
		if v != None:
			notes_mod_all = Note.objects.allowed(v.id).filter(uploader=user_id).distance(v.position).order_by("distance")
			notes_mod = notes_mod_all[from_limit:to_limit]
			total_elems = len(notes_mod_all)
		else:
			notes_mod = Note.objects.filter(uploader=user_id)
			notes_mod = notes_mod_all[from_limit:to_limit]
			total_elems = len(notes_mod_all)
		notes = []
		for note in notes_mod:
			try:
				n = note.get_dictionary(viewer=v)
				notes += [n]
			except:
				pass
		return notes, total_elems
	except:
		return [], 0 
	
def delete(note_id, user_id):
	"""
	@deprecated: use the node delete instead
	Deletes the note indicated
	"""
	try:
		n = Note.objects.get(pk = note_id)
		if user_id == n.uploader.id or user_id==n.uploader:
			n.delete()
		else:
			return False, "You can't delete this note because it is not yours"
		return True, "No error"
	except:
		return False, "This note doesn't exist"