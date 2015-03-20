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

from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response
import zipfile
import time
import simplejson
import hashlib
import random
import os

FORMAT="format"
XML_FORMAT = "XML"
JSON_FORMAT = "JSON"
XML_ZIP_FORMAT = "XML.ZIP"
JSON_ZIP_FORMAT = "JSON.ZIP"
FORMATS = [XML_FORMAT, JSON_FORMAT, XML_ZIP_FORMAT, JSON_ZIP_FORMAT]


MIMETYPES = { JSON_FORMAT : "application/json; charset=UTF-8",
              XML_FORMAT : "text/xml",
              JSON_ZIP_FORMAT : "application/zip",
              XML_ZIP_FORMAT : "application/zip",
            }
          
def rand_name():
    m = hashlib.md5()
    m.update(str(random.random()))
    return m.hexdigest()        

def getResponseFormat(request):
    """
    Looks for a specified format
    """
    try:
        format = request.GET [FORMAT].upper()           
        if format in FORMATS:
            return format                                 
        else:               
            return XML_FORMAT
    except:          
        return XML_FORMAT
    
def compress_data(data):
    zip_name = "/tmp/%s" % rand_name()
    
    file = zipfile.ZipFile(zip_name, "w")
    now = time.localtime(time.time())[:6]
    
    info = zipfile.ZipInfo("data")
    info.date_time = now
    info.compress_type = zipfile.ZIP_DEFLATED
    file.writestr(info, data.encode("utf-8"))
    file.close()
    new_data = open(zip_name, "rb").read()
    os.remove(zip_name)
    return new_data
  
def generateResponse (format, data_hash, template):
    """
    Renders the template with the correct format
    """
    c = Context(data_hash)            
    if format in (JSON_FORMAT, JSON_ZIP_FORMAT):
        template="%s.json" % (template)
        t = loader.get_template(template)
        mime_type = MIMETYPES[format]
        data = eval(t.render(c))   # Transform the text into a dictionary
        data = simplejson.dumps(data) # Transform the dictionary into  a correct json object
        if format == JSON_ZIP_FORMAT:
            data = compress_data(data)

    else:
        template="%s.xml" % (template)
        t = loader.get_template(template)
        mime_type = MIMETYPES[format]
        data = t.render(c)
        if format == XML_ZIP_FORMAT:
            data = compress_data(data)
    return HttpResponse(data, mime_type)
              
            
              
            
            
            
            
            
            
            
    
