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


#from Channels.C_11870Channel import *
#from Channels.PanoramioChannel import * 
from GoogleApi.GoogleTranslate import *

from libLGS.Auth import *
from libLGS.PhotosManager import *
from libLGS.Nodes.Photo import *
from libLGS.Privacy import *

import httplib, urllib



if __name__ == "__main__":


	lgs = Auth()
	lgs.login('jgato','jgato')
	
	params = urllib.urlencode ({'userid': '475', 'photo_id':'35249'})
	
	data = Auth().do_petition("/social/user/set_avatar/", params, "POST" )
	
	print data.read()
	res = simplejson.load(data)
	
	print res

#	pm = PhotosManager()
#
#	myphoto = Photo()
#	myphoto.name = "prueba"
#	myphoto.description = "descripcion"
#	myphoto.latitude = 0.0
#	myphoto.longitude = 0.0
#	myphoto.altitude = 0.0
#	myphoto.path = "/tmp/wallpaper.png"
#	
#	photo_id = pm.add_photo (myphoto)
#
#	if (photo_id != -1):
#		ret = pm.set_privacy (photo_id, Privacy.PUBLIC)
#		if (ret != -1):
#			print "[*] New photo uploaded (%s)" % (photo_id)
#		else:
#			print "Error while photo was added (%s)" % (photo_id)



					
	
	
