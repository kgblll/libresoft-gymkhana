#
# Copyright (C) 2009-2010 GSyC/LibreSoft, Universidad Rey Juan Carlos
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
#	Author : Jose Gato Luis <jgato@libresoft.es>
#

from social.core import config

class Social_Core_Exception(Exception):
	pass

class Social_Date_Exceptions(Exception):
	pass

class Social_Video_Exceptions(Exception):
	pass

VIDEO_NOT_SUPPORTED = Social_Video_Exceptions ("Social video codecs not supported")

NODE_NOT_IMAGE = Social_Core_Exception ("Social Node does not have info for image")
NODE_NOT_SOUND = Social_Core_Exception ("Social Node does not have info for sound")
NODE_NOT_VIDEO = Social_Core_Exception ("Social Node does not have info for video")
NODE_NOT_EXIST_OR_PERM = Social_Core_Exception ("Social Node does not exist or you dont have perms")

DATE_TIME_FORMAT_ERROR = Social_Date_Exceptions ("Date format error, it should be:" + config.EXPIRATION_DATE_FORMAT)
DATE_TIME_FUTURE = Social_Date_Exceptions ("Date has to be allocated in the future")
DATE_TIME_NOT_LATER = Social_Date_Exceptions ("Date incorrect: avaliable_to field has to be later than avaliable_from")