#!/usr/bin/env python

# Copyright (C) 2009-2010 GSyC/LibreSoft, Universidad Rey Juan Carlos
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Authors : Roberto Calvo <rocapal@gsyc.es>

import sys

from GenericItem import *

class PhotoItem (GenericItem):

	def __init__ (self):
		self.type = SUPPORTED_ITEMS["photo_item"]
		self.name = None
		self.description = None
		self.external_info = { "info_url": None, "photo_thumb": None, "photo_url": None}
		