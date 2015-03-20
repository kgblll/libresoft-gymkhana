# Copyright (C) 
#
#  Author : 

from GIC.Channels.GenericChannel import *


class ChannelTest (GenericChannel):

    # mandatory fields to work on LibreGeoSocial search engine
    
	MANDATORY_FIELDS = ["latitude", "longitude", "radius", "category"]
	
	CATEGORIES = [{"id" : "0", "name" : "all", "desc" : "All supported categories "},
				  {"id" : "1", "name" : "category1", "desc" : "Category for..."},
				  ]


	def __init__ (self):
		self.options = {}
		
	def get_categories(self):
		return self.CATEGORIES	
		
	def get_info(self):
		return "Channel description"
	
	def set_options(self, options):
		"""
		 Fill self.options with the received dictionary
		 regarding mandatory and optional fields of your channel
		"""
		
		return True, ""

	def process (self):
		"""
	 	 Make the search and return the nodes
		"""	
	