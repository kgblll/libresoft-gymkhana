#
#  Copyright (C) 2009 GSyC/LibreSoft
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
#    Author : Jose Antonio Santos Cadenas <jcaden __at__ gsyc __dot__ es>
#

#Photos configuration
MAX_PHOTO_UPLOAD_SIZE = 500 #KB
MAX_PHOTO_WIDTH = 900   #pixels
MAX_PHOTO_HEIGHT = 900  #pixels
MAX_ICON_UPLOAD_SIZE = 12 #KB
MAX_VIDEO_UPLOAD_SIZE = 3000 #KB

SUPPORTED_TYPES = ["JPEG", "GIF", "BMP", "PNG"] #image types supported 

#Search configuration
ALLOWED_SEARCH = ["photo", "person", "note", "sound", "video"]

#node icons
DEFAULT_NODE_ICON = "/social/layer/lgs/icon"

EXPIRATION_DATE_FORMAT = "%H:%M:%S-%Y/%m/%d %Z"
