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

class Layer_Does_Not_Exist(Exception):
	pass

class Layer_Perms(Exception):
	pass

class Layer_Node(Exception):
	pass

LAYER_DOES_NOT_EXIST = Layer_Does_Not_Exist ("Layer does not exist")

LAYER_EXTERNAL_NOT_DELETE_NODES = Layer_Perms ("You cannot delete nodes in external layers")
LAYER_EXTERNAL_NOT_CREATE_NODES = Layer_Perms ("You cannot create nodes in external layers")
LAYER_EXTERNAL_NOT_MODIFY = Layer_Perms ("You cannot modify external layers")
LAYER_NOT_WRITE = Layer_Perms ("You cannot modify this layer, not writeable perms")
LAYER_NOT_OWNER = Layer_Perms ("You cannot modify this layer's info, you are not the owner")

LAYER_NOT_NODE = Layer_Node ("Node not included in the layer")