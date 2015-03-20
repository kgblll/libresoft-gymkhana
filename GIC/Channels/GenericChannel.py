#!/usr/bin/env python

# Copyright (C) 2009-2010 GSyC/LibreSoft, Universidad Rey Juan Carlos
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


class GenericChannel:

	def __init__ (self):
		pass
		
	def get_info(self):
		pass
	
	def set_options(self, options):
		pass
	
	def set_search_pattern (self,pattern):
		self.search_pattern = pattern

	def get_items (self):
		pass

	
