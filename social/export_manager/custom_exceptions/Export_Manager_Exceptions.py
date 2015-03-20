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



class Export_Manager_Exception(Exception):
	pass

EXPORT_MANAGER_CONFIGURATION_ERROR = Export_Manager_Exception ("Export manager is not correctly configured")
EXPORT_MANAGER_ENGINE_EXPORT_NOT_EXIST = Export_Manager_Exception ("Export manager: engine not exist to export")
EXPORT_MANAGER_ENGINE_OUTPUT_NOT_EXIST = Export_Manager_Exception ("Export manager: engine not exist to output")
EXPORT_MANAGER_NO_SOCIAL_NODES = Export_Manager_Exception ("Export manager: no social nodes to export")