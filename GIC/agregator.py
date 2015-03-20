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


from Channels.C_11870Channel import *
from Channels.PanoramioChannel import * 
from GoogleApi.GoogleTranslate import *
from libLGS.Auth import *
from libLGS.NotesManager import *
from libLGS.PhotosManager import *
from libLGS.Nodes.Photo import *
from libLGS.Privacy import *

import httplib, urllib

def agregator(category, num_elements):
	
	c = C_11870Channel ("Place")
	
	c.set_config_by_pattern (category,num_elements)
	l = c.process()

	gt = GoogleTranslate()
	lnotes = []
	
	for place in l:

		
		try:
			place.summary = place.summary[:500]
			place.summary = "[11870-" + category + "]" + place.summary
		except:
			place.summary = "[11870-" + category + "]"


		place.summary = gt.translate(place.summary.encode("utf-8"))


		mynote = Note()
		mynote.id = 0
		mynote.title = place.title
		mynote.text = place.summary
		mynote.latitude = place.latitude
		mynote.longitude = place.longitude

		lnotes.append(mynote)

#		print place.title + " - " + place.service + " - " + place.summary + " - (%s %s)" % (place.latitude, place.longitude)
	

	return lnotes

if __name__ == "__main__":


	lgs = Auth()
	lgs.login('rocapal','rocapal')

	pm = PhotosManager()

	myphoto = Photo()
	myphoto.name = "prueba"
	myphoto.description = "descripcion"
	myphoto.latitude = 0.0
	myphoto.longitude = 0.0
	myphoto.altitude = 0.0
    myphoto.path = "/tmp/wallpaper.png"
	
	photo_id = pm.add_photo (myphoto)

	if (photo_id != -1):
		ret = pm.set_privacy (photo_id, Privacy.PUBLIC)
		if (ret != -1):
			print "[*] New photo uploaded (%s)" % (photo_id)
		else:
			print "Error while photo was added (%s)" % (photo_id)


	exit(-1)


	if (len(sys.argv) < 3):
		print "Usage: %s pattern num_elements [sim]" % (sys.argv[0])
		exit(-1)

	# check the simulation
	simulate = 0
	
	if (len(sys.argv) == 4 and sys.argv[3] == "sim"):
		print "-> Simulation active!"
		simulate = 1
		
	lnotes = agregator(sys.argv[1],sys.argv[2])
	
	lgs = Auth()
	lgs.login('rocapal','rocapal')

	nm = NotesManager()

	for note in lnotes:

		if (simulate == 1):
			print "[*]" + note.title + " - " + note.text + " - (" + note.latitude + " " + note.longitude + ")"

		else:
		
			note_id = nm.add_note(note)
		
			if (note_id != -1):
				ret = nm.set_privacy(note_id, NotesManager.PUBLIC)
				if (ret != -1):
					print "[*] New note added (%s)" % (note_id)
				else:
					print "Error while note was added (%s)" % (note_id)
					
	
	
