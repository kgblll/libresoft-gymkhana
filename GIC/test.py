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

def test():

	
	
	c = C_11870Channel("Place")
	
	c.set_config_by_coordenates( "", "40.335537", "-3.867252", "1.0", "20")
	
	c.process()
	

#	p = PanoramioChannel("Photo")
#	p.set_config( "", "40.335537", "-3.867252", "1.0")

#	p.process()
	

if __name__ == "__main__":
	test()
		
