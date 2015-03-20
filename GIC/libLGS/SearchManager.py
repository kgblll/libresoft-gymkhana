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
#  Author : Jose Gato Luis <jgato@libresoft.es>
#
#


from Auth import *
from Privacy import *
import simplejson
from MultiPart import *
from Nodes.Photo import Photo, SemanticPhoto
from Nodes.Note import Note

class SearchManager():


	format_json = "&format=JSON"
	url_semantic_create = "/semanticSearch/social/search/semantic/?word="
	url_create = "/social/search/?terms="
	url_options = "&sense=0&checkPhotos=True&checkNotes=True" 

	similarityInfo_fields = ["value", "word1", "word2"]
	position_fields = [ "latitude", "longitude", "altitude", "radius", "since"]
	photo_fields = [ "name", "description"]
	note_fields = [ "title", "text"]

	def __init__ (self):
		None
		
	def _to_social_photo (self, photo):
		socialPhoto = SemanticPhoto()
		
		socialPhoto.id = photo["id"]

		if "similarity" in photo:
			similarityInfo = photo["similarity"]
		
			for field in self.similarityInfo_fields:
				setattr(socialPhoto, field, similarityInfo[field])

		if "position" in photo:
			position = photo["position"]
		
			for field in self.position_fields:
				setattr(socialPhoto, field, position[field])

		for field in self.photo_fields:
			setattr(socialPhoto, field, photo[field])

		return socialPhoto

	def _to_social_note (self, note):
		socialNote = Note()

		if "similarity" in note:
			similarityInfo = note["similarity"]
		
			for field in self.similarityInfo_fields:
				setattr(socialNote, field, similarityInfo[field])

		if "position" in note:
			position = note["position"]

			for field in self.position_fields:
				setattr(socialNote, field, position[field])

		for field in self.note_fields:
			setattr(socialNote, field, note[field])

		return socialNote


	def make_search (self, keyword, enableSemantic = False):

		if enableSemantic is True:
			url = self.url_semantic_create + keyword + self.url_options + self.format_json
		else:
			url = self.url_create + keyword + self.format_json

		data = Auth().do_petition(url, "", "GET", None, None)

		res = simplejson.load(data)

		#res = {'code': '200', 'results': {'note': [], 'photo': [{'name': 'Climbing the Mountain', 'similarity': {'word1': 'mountain', 'value': 200.0, 'word2': 'Mountain'}, 'since': '2009-11-18 16:37:01.989876', 'uploader': {'username': 'prueba', 'status': {'message': '', 'since': '2009-11-16 11:30:06.689425'}, 'first_name': 'prueba', 'last_name': 'prueba', 'name': 'prueba prueba', 'tags': [], 'since': '2009-11-16 11:30:06.689180', 'email': 'jgato@gsyc.es', 'position': {'latitude': 0.0, 'altitude': 0.0, 'since': '2009-11-16 11:30:06.689581', 'radius': 0.0, 'longitude': 0.0}, 'type': 'person', 'id': 2}, 'position': {'latitude': 28.35829, 'altitude': 0.0, 'since': '2009-11-18 16:37:01.989844', 'radius': 0.0, 'longitude': -81.586145999999999}, 'type': 'photo', 'id': 549, 'tags': ['2009', 'animal', 'Animal', 'climbing', 'climb', 'lift', 'sunrise', 'sun', 'Katie', 'PirateTinkerbell', 'morning', '3/9/2009', '3/9/09', '09', '3/9', '3/09', '3/2009', 'March', 'Monday', '9', '9,', 'Monday,', 'WDW', 'Walt', 'Disney', 'World', 'Florida', 'FL', 'Orlando', 'Orlando,', 'Parks', "Disney's", 'Kingdom', 'kingdom', 'AK', 'ROOF', 'Everest', 'Expedition', 'Mountain', 'mountain', 'Yeti', 'Asia', 'snow', 'train'], 'description': '[flickr-anm]Gotta love that bright morning sun right after it rises!  This is a great view off the mountain at this point in the ride!\n\nTaken on-ride on Expedition Everest!'}, {'name': 'Climbing the Mountain', 'similarity': {'word1': 'mountain', 'value': 200.0, 'word2': 'mountain'}, 'since': '2009-11-18 16:37:01.989876', 'uploader': {'username': 'prueba', 'status': {'message': '', 'since': '2009-11-16 11:30:06.689425'}, 'first_name': 'prueba', 'last_name': 'prueba', 'name': 'prueba prueba', 'tags': [], 'since': '2009-11-16 11:30:06.689180', 'email': 'jgato@gsyc.es', 'position': {'latitude': 0.0, 'altitude': 0.0, 'since': '2009-11-16 11:30:06.689581', 'radius': 0.0, 'longitude': 0.0}, 'type': 'person', 'id': 2}, 'position': {'latitude': 28.35829, 'altitude': 0.0, 'since': '2009-11-18 16:37:01.989844', 'radius': 0.0, 'longitude': -81.586145999999999}, 'type': 'photo', 'id': 549, 'tags': ['2009', 'animal', 'Animal', 'climbing', 'climb', 'lift', 'sunrise', 'sun', 'Katie', 'PirateTinkerbell', 'morning', '3/9/2009', '3/9/09', '09', '3/9', '3/09', '3/2009', 'March', 'Monday', '9', '9,', 'Monday,', 'WDW', 'Walt', 'Disney', 'World', 'Florida', 'FL', 'Orlando', 'Orlando,', 'Parks', "Disney's", 'Kingdom', 'kingdom', 'AK', 'ROOF', 'Everest', 'Expedition', 'Mountain', 'mountain', 'Yeti', 'Asia', 'snow', 'train'], 'description': '[flickr-anm]Gotta love that bright morning sun right after it rises!  This is a great view off the mountain at this point in the ride!\n\nTaken on-ride on Expedition Everest!'}]}}
		#print res

		if  (res['code'] != "200"):
			return -1
		else:
			results = res["results"]
			notes = results["note"]
			photos = results["photo"]

			socialNotes = []
			socialPhotos = []
			for note in notes:
				socialNotes.append (self._to_social_note (note))

			for photo in photos:
				socialPhotos.append (self._to_social_photo (photo))

			return {"notes": socialNotes, "photos": socialPhotos}



																							
