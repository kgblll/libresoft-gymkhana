#
#  Copyright (C) 2010 GSyC/LibreSoft
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
#    Author : Raul Roman Lopez <rroman __at__ libresoft __dot__ es>
#
from opencv import cv
from math import sqrt

class ComparisonManager:
	
	
	def __init__(self):
		self.matched_id = -1
		self.matched_goodness = 1000

		## Decision constants
	        self.MATCH_THRESHOLD = 0.2
	        self.GOODNESS_THRESHOLD = 0.2
	
        	## SURF constants
        	self.EXTENDED = 0
        	self.HESSIAN_THRESHOLD = 3000
        	self.NOCTAVES = 3
	        self.NOCTAVELAYERS = 1

	
	def getResults(self):
		return self.matched_id, self.matched_goodness

	def extractSURFPoints(self, path):
		print path
		image = cv.LoadImage(path, cv.CV_LOAD_IMAGE_GRAYSCALE)
		(keypoints, descriptors) = cv.ExtractSURF(image, None, cv.CreateMemStorage(), (self.EXTENDED, self.HESSIAN_THRESHOLD, self.NOCTAVES, self.NOCTAVELAYERS))
		return keypoints, descriptors

	def compareTwoPhotos(self, path1, path2, data=None):
		''' This function returns the number of matching points and the goodness of the election (their mean) '''
		kp1, dp1 = self.extractSURFPoints(path1)
		if data:
			kp2 = data[0]
			dp2 = data[1]
		else:
			kp2, dp2 = self.extractSURFPoints(path2)
		
		npoints2 = 0
		mean = 0
		for i in range(len(kp1)):
			last_value1 = 500000
			last_value2 = 500000
			dsc1 = dp1[i]
			lapl1 = kp1[i][1]
			for k in range(len(kp2)):
				# if laplacian signs doesn't match, discard the point
				lapl2 = kp2[k][1]
				if lapl1 != lapl2:
					continue
				
				dsc2 = dp2[k]
				value = 0
				for j in range(len(dsc1)):
					value = value + pow(dsc1[j] - dsc2[j], 2)
				value = sqrt(value)
				if value < last_value1:
					last_value2 = last_value1
					last_value1 = value
					point = kp2[k][0]
				elif value < last_value2:
					last_value2 = value
			if (abs(last_value1 - last_value2) > self.MATCH_THRESHOLD):
				npoints2 += 1
				mean += last_value1
		print "Matched: %d" % (npoints2)
		if npoints2 < 2:
			return None, None
		else:
			mean = mean/npoints2
		print "Matched: %d; Mean: %f" % (npoints2, mean)
		if mean < self.GOODNESS_THRESHOLD:
			return (npoints2, mean)
		return None, None

