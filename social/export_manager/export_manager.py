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

from custom_exceptions.Export_Manager_Exceptions import *


class Export_Manager():
	
	exportEngine = None
	outputEngine = None

	def __init__(self):
		pass
	
	def configure(self, exportEngine, outputEngine, backup = False, viewer = None):
		
		try:
			exportEngineModule = exportEngine.lower()
			obj = __import__("social.export_manager.export_engine.%s" % (exportEngineModule), globals(), locals(), [exportEngineModule], 0)
			engine = eval ("obj." + exportEngine + "()")
			self.exportEngine = engine
		except Exception:
			raise EXPORT_MANAGER_ENGINE_EXPORT_NOT_EXIST
		try:
			outputEngineModule = outputEngine.lower()
			obj = __import__("social.export_manager.output_engine.%s" % (outputEngineModule), globals(), locals(), [outputEngineModule], 0)
			engine = eval ("obj." + outputEngine + "()")
			self.outputEngine = engine
		except Exception:
			raise EXPORT_MANAGER_ENGINE_OUTPUT_NOT_EXIST
	
		if backup:
			self.exportEngine.setIncludeBinaries()
		
		if viewer is not None:
			self.exportEngine.setViewer(viewer)
			
	def _test_nodes(self, nodes):
		
		from social.core.models import Social_node
		
		for node in nodes:
			if not isinstance(node, Social_node):
				return False
		return True

	def export(self, socialNodes, extraInfo = None, viewer = None):
	
		if self.exportEngine == None or self.outputEngine == None:
			raise EXPORT_MANAGER_CONFIGURATION_ERROR
		
		if self._test_nodes(socialNodes) == False:
			raise EXPORT_MANAGER_NO_SOCIAL_NODES

		# configure the export engine
		self.exportEngine.addNodeList(socialNodes)
		if extraInfo is not None:
			self.exportEngine.setExtraInfo(extraInfo)
		
		data = self.exportEngine.export()

		#configure the output engine
		self.outputEngine.setMIMEType(self.exportEngine.getMIMEType())
		self.outputEngine.setData(data)
		
		return self.outputEngine.output()
	
		
		
		