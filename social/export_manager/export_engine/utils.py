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

import zipfile
import random
import time
import hashlib
import os, tempfile
from settings import BASEDIR 


TMP_DIR = os.path.join(BASEDIR, "tmp")

def rand_name():
	m = hashlib.md5()
	m.update(str(random.random()))
	return m.hexdigest()

def file_temp(file_suffix = ""):
	(fd, fname) = tempfile.mkstemp(suffix = file_suffix)
	print fd, fname
	return os.fdopen(fd, "w+b")

def file_temp_hide(file_suffix = ""):
	#using this function the temp file is going to be deleted as soon is invoked close method
	#even if this is used by garbage collector
	
	file = tempfile.TemporaryFile(mode='w+b',suffix = file_suffix, dir = TMP_DIR)
	return file

def compress_data(data, into = None, binary_file = False, extra_file_name = None):
	
	if into is None:
		into = file_temp_hide(".zip")
	
	file = zipfile.ZipFile(into, "a")
	
	
	now = time.localtime(time.time())[:6]
	file.date_time = now
	file.compress_type = zipfile.ZIP_DEFLATED
	
	
	if binary_file:
		file.write(data.name, os.path.basename(data.name))
	else:
		if extra_file_name is None:
			extra_file_name = "data"
			
		info = zipfile.ZipInfo(extra_file_name, now)
		info.external_attr = 0400 << 16L
		info.compress_type = zipfile.ZIP_STORED
		file.writestr(info, data.encode("utf-8"))
		
	
	file.close()
	return file
