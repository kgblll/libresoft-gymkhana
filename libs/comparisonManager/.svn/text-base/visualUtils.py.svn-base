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

import cv

def extractSURFPoints(data, width, height):
	image = cv.CreateImageHeader((width, height), cv.IPL_DEPTH_8U, 3)
	cv.SetData(image, data, width)
	(keypoints, descriptors) = cv.ExtractSURF(image, None, cv.CreateMemStorage(), (0, 3000, 3, 1))
	return keypoints, descriptors

def compareTwoPhotos((kp1, dp1), (kp2, dp2)):
	''' This function returns the number of matching points and the goodness of the election (their mean) '''
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
			if (lapl1+lapl2) == 0:
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
		if (abs(last_value1 - last_value2) > 0.2):
			npoints2 += 1
			mean += last_value1
	
	if npoints2 == 0:
		mean = 1000
	else:
		mean = mean/npoints2
	return (npoints2, mean)

