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

from generic_output_engine import Generic_Output_Engine
from custom_exceptions.output_engine_exceptions import *
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
import mimetypes

class HTTPResponse (Generic_Output_Engine):
	
	# supported mimetypes and a value true or false regarding the data should be attached in the response
	supportedMimeTypes = { "text/plain" : False, "application/json; charset=UTF-8" : False, "application/zip" : True, 
						"text/xml" : False}
	attachment = True
	mimeType = "text/plain"
	data = None
	
	def __init__(self):
		pass
	
	def setMIMEType(self, mimeType):
		if mimeType in self.supportedMimeTypes:
			self.mimeType = mimeType
		else:
			raise OUTPUT_ENGINE_NOT_SUPPORT_MIME_TYPE
		
	def setData(self, data):
		self.data = data
		
	def output(self):

		if self.supportedMimeTypes[self.mimeType]:
			wrapper = FileWrapper(self.data)
			response = HttpResponse(wrapper, mimetype=self.mimeType)
			response['Content-Disposition'] = 'attachment; filename=content.zip'
			response['Content-Length'] = self.data.tell()
			self.data.seek(0)
		else:
			response = HttpResponse(self.data, mimetype=self.mimeType)
		
		
		
		return response

		