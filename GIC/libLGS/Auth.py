#!/usr/bin/env python
# -*- coding: utf-8 -*-


#  Copyright (C) 2009 GSyC/LibreSoft
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



import httplib, urllib, urllib2


class Auth ( object ):
	
	# storage for the instance reference
	_instance = None                    

	class Singleton:
		
		mUrl = "test.libregeosocial.libresoft.es"
		mUrlLogin = "/social/user/login/"
		mHeaders = None
		mSession = None

		def __init__(self):
			pass

		def setServer(self, server):
			self.mUrl = server

		def login (self, login, password, secure = True):
			
			self.mLogin = login
			self.mPassword = password
			
			params = urllib.urlencode({'username': self.mLogin,'password': self.mPassword})
			headers = {"Content-type": "application/x-www-form-urlencoded","Accept":"text/plain"}

			if secure:
				con = httplib.HTTPSConnection(self.mUrl)
			else:
			    con = httplib.HTTPConnection(self.mUrl)
			     
			con.request("POST",self.mUrlLogin,params,headers)
			data = con.getresponse()

			self.mHeaders = data.getheader('set-cookie')
			self.mCookie = {"Cookie": self.mHeaders}
			
			self.mSession = self.mHeaders.split(";")[0]
			
			
		def do_petition (self, urlPath, params, petition_type = "POST", https = None, content_type = None):

			
			headers = {"Content-type": "application/x-www-form-urlencoded",
					   "Accept": "text/plain",
					   "Cookie": self.mSession }

			if not (content_type is None):
				headers["Content-type"] = content_type

			
			con = None

			if https is None:
				con = httplib.HTTPConnection(self.mUrl)
			else:
				con = httplib.HTTPSConnection(self.mUrl)

			if (petition_type == "POST"):
				con.request ("POST",urlPath,params,headers)
			else:
				con.request ("GET",urlPath,params,headers)
				

				#con.putheader("Cookie",self.mHeaders.split(";")[0])
				#con.endheaders()
		

			data = con.getresponse()
			
			return data
	
		

	def __init__ (self):
		
		if Auth._instance is None:
			Auth._instance = Auth.Singleton()

		self.__dict__['_EventHandler_instance'] = Auth._instance

	def __getattr__(self, aAttr):
		return getattr(self._instance, aAttr)

	def __setattr__(self, aAttr, aValue):
		return setattr(self._instance, aAttr, aValue)
