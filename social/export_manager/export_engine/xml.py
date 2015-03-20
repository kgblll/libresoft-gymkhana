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

from generic_export_engine import Generic_Export_Engine
from social.privacy.exceptions import PermissionError
from social.core.utils import get_person


from django.template import Context, loader

import utils, os

class xml (Generic_Export_Engine):
		
	ZIP_FORMAT = "application/zip"
	XML_FORMAT = "text/xml"

	
	def __init__(self, compress = False, binaries = False, viewer= None):
		self.nodesList = []
		self.extraInfo = None
		self.mimeType = self.XML_FORMAT
		self.zip_backup = None
		
		self.compress = compress
		
		self.includeBinaries = binaries
		if binaries:
			self.mimeType = self.ZIP_FORMAT
			
		if viewer is not None:
			self.user = get_person(viewer)
		else:
			self.user = None
		
	def setIncludeBinaries(self):
		self.includeBinaries = True
		self.mimeType = self.ZIP_FORMAT
		if self.zip_backup is None:
			self.zip_backup = utils.file_temp_hide(".zip")

	def setViewer(self, viewer):
		self.user = get_person(viewer)
		
	def getMIMEType(self):
		return self.mimeType
	
	def addNode(self, node):
		
		if self.includeBinaries:
			try:
				object = open(node.get_path(self.user))
				utils.compress_data(object, into = self.zip_backup, binary_file = True )
				node.info_url =  "file://" + os.path.basename(object.name)
			except: #fix: we should have a better way to detect nodes without binaries
				pass
		self.nodesList.append(node)
	
	def addNodeList(self, nodeList):
		for node in nodeList:
			self.addNode(node)
	
	def setExtraInfo(self, extraInfo):
		self.extraInfo = extraInfo
	

	def _xmlTemplate(self, data):
		c = Context(data)			
		
		template="node/list.xml" 
		t = loader.get_template(template)
		data = t.render(c)   # Transform the text into a dictionary
		
		if self.compress:
			data = utils.compress_data(data)
		
		return data

			
	def export(self, viewer = None):
		
		#we have to extract the dictionaries of each node
		
		nodesDictList = []
		
		user = get_person(viewer)
		
		for node in self.nodesList:
			try:
				nodesDictList += [node.get_node().get_dictionary(user)]
			except PermissionError:
				print "permission error"
				pass
		
		data = { "results" : nodesDictList,
				"elems" : len(nodesDictList),
				"code" : "200"}
		
		if self.extraInfo:
			data.update(self.extraInfo)
			
		data_template = self._xmlTemplate(data)
		
		if self.includeBinaries:
			utils.compress_data(data_template, self.zip_backup, False, "data.xml")
			return self.zip_backup
		else:
			return data_template 
			
