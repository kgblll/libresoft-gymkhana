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
#  Author : Roberto Calvo Palomino <rocapal@gsyc.es>
#
#

from Nodes.Note import *
from Auth import *
import simplejson

class NotesManager ():

	(
		PRIVATE,
		FRIENDS,
		FRIENDS_OF_FRIENDS,
		PUBLIC
	) = range (4)

	privacy = {1:"friends", 2:"friends_of_friends", 3:"public"}
	

	format_json = "?format=JSON"
	url_create = "/social/note/create/" + format_json
	url_get_data = "/social/note/%s/data/"
	url_set_privacy = "/social/note/%s/privacy/allow/" + format_json


	def __init__(self):
		None


	def add_note (self, note):

		params = urllib.urlencode({'title': note.title.encode("utf-8"),
								   'text': note.text.encode("utf-8"),
								   'latitude': note.latitude,
								   'longitude': note.longitude })
		
		data = Auth().do_petition(self.url_create, params, "POST" )

		res = simplejson.load(data)
		
		if  (res['code'] != "200"):
			return -1

		return res['id']

		

	def set_privacy (self, note_id, level):

		params = urllib.urlencode ({'role': self.privacy[level]})
		url = self.url_set_privacy % (note_id)

		data = Auth().do_petition(url, params, "POST" )
		
		res = simplejson.load(data)

		if  (res['code'] != "200"):
			return -1

		return 0
	
