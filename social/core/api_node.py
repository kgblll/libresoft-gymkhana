#
#  Copyright (C) 2009-20010 Universidad Rey Juan Carlos, GSyC/LibreSoft
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
#	Author : Jose Antonio Santos Cadenas <jcaden __at__ gsyc __dot__ es>
#

from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D 
from django.core.exceptions import MultipleObjectsReturned

from social.privacy.utils import is_allowed
from social.core.utils import get_default_layer

from datetime import datetime
from models import Social_node, Tag, Comment, Person, Layer
from utils import get_person, check_later_date, check_expiration_time
from social.core.config import EXPIRATION_DATE_FORMAT
from social.core.custom_exceptions.social_core_exceptions import Social_Date_Exceptions

def set_privacy(node_id, privacy_choice, change_profile = True, field = None):
	"""
	   set the node_id privacy to privacy_choice. If change_profile = True
	   then the node privacy is changed to privacy_choice, if False it will change
	   only the privacy of field.
	   If field is not None, the it will change the privacy of the field.
	   change_profile = False and field = None it has no effects. 
	"""
	
	from social.privacy2.utils import get_privatizable_fields
	
	if field:
		if field not in get_privatizable_fields():
			return False, "Privacy for field %s not allowed" % (field)
	
	try:
		node = Social_node.objects.get(id = node_id)
	
		if not node.set_perm(privacy_choice):
			return False, "Error changing perms"
		
		if field != None and not node.set_perm_field(field, privacy_choice):
			return False, "Error changing field perms"
		
		return True, ""	
	except:
		return False, "Node doesn't exist"
	
	
def set_privacy_default(node_id):
	"""
	   set the node privacy and node position to
	   public. It is useful if we want to create nodes
	   public by default.
	"""

	return set_privacy(node_id, "Public", True, "position")


def set_layer(node_id, layer_id = None):
	"""
	   set the node inside the layer: layer_id.
	   if layer_id = None the it will be used the id
	   of the default layer in the system
	"""
	
	try:
		if layer_id == None:
			layer_id = get_default_layer(None)["id"]
			
		
		node = Social_node.objects.get(id = node_id)
		layer = Layer.objects.get(id = layer_id)
		if not layer.set_node(node.id):
			return False, "Error setting node to layer"

		return True, ""	
	
	except MultipleObjectsReturned:
		return False, "Error more than one default layer"
	except Exception, err:
		print err
		return False, "Error setting node to default layer"



def set_tag(nodeid, tags):
	"""
	Sets new tags to the social node
	
	@param nodeid: (int) with the node id
	@param tags: (str) A string with all the tags separated by spaces
	
	@return: a tuple (bool, str) with the result (correct or not) and a description
	"""
	try:
		node=Social_node.objects.get(id=nodeid)
	except:
		return False, "Node doesn't exist"
	for tag in tags.split():
		tag_obj, created=Tag.objects.get_or_create(tag=tag)
		node.tags.add(tag_obj)
	return True, "No error"

def remove_tag(nodeid, tags):
	"""
	Removes tags from the social node
	
	@param nodeid: (int) with the node id
	@param tags: (str) A string with all the tags separated by spaces
	
	@return: a tuple (bool, str) with the result (correct or not) and a description
	"""
	try:
		node=Social_node.objects.get(id=nodeid)
	except:
		return False, "Node doesn't exist"
	for tag in tags.split():
		try:
			tag_obj=Tag.objects.get(tag=tag)
			node.tags.remove(tag_obj)
		except:
			pass
	return True, "No error"

def set_coordinates(nodeid, latitude, longitude, **kargs):
	"""
	Sets the position of any type of social_node
	"""
	try:
		n = Social_node.objects.get(pk=nodeid)
		n.position = Point(float(longitude), float(latitude), srid=4326)
		if "radius" in kargs:
			n.radius=float(kargs["radius"])
		if "altitude" in kargs:
			n.altitude = float(kargs["altitude"])
		n.pos_time = datetime.now()
		n.save()
		return True, "No error"
	except:
		return False, "The node doesn't exist"

def set_icon(nodeid, uri = None):
	"""
	Sets an icon uri for the node with nodeid
	"""
	try:
		node=Social_node.objects.get(id=nodeid)
	except:
		return False, "Node doesn't exist"
	
	if uri is not None:
		node.icon = uri
	else:
		node.icon = "defaultpath"

	return True, "No error"
	
def set_comment(nodeid, comment, author):
	"""
	Sets a comment made by author to the node with nodeid
	"""
	try:
		n = Social_node.objects.get(pk=nodeid)
	except:
		return False, "The node doesn't exist"
	try:
		a = Person.objects.get(pk=author)
	except:
		return False, "Author doesn't exist"
	if is_allowed(n.get_node(), a):
		c = Comment(node=n, author=a, comment=comment)
		c.save()
		return True, "Comment created correctly"
	else:
		return False, "You are not allowed to comment this node"

def set_dates(node_id, avaliable_from, avaliable_to):
	"""
	Sets avaliable dates of a node
	"""
	
	try:
		node = Social_node.objects.get(pk=node_id)
	except:
		return False, "The node doesn't exist"
	
	if avaliable_from is not None:
		avaliable_from = datetime.strptime(avaliable_from, EXPIRATION_DATE_FORMAT)
	else:
		avaliable_from = node.avaliable_from
		
	if avaliable_to is not None:
		avaliable_to = datetime.strptime(avaliable_to, EXPIRATION_DATE_FORMAT)
	else:
		avaliable_to = node.avaliable_to
		
	try:
		if avaliable_to is not None:
			check_expiration_time(avaliable_to)	
			if avaliable_from is not None:
				check_later_date(avaliable_from, avaliable_to)
	except Social_Date_Exceptions, err:
		print err
		raise err
	except Exception, err:
		print err
		return err
	
	
	#in this point there are no exceptions so the node dates are correct
		
	if avaliable_from is not None:
		node.avaliable_from = avaliable_from
		
	if avaliable_to is not None:
		node.avaliable_from = avaliable_from
	print node
	node.save()
	
	
def delete(node_id, viewer):
	"""
	Deletes the photo indicated
	"""
	try:
		node = Social_node.objects.get(pk = node_id)
	except:
		return False, "This Node doesn't exist"
	
	try:
		person = Person.objects.get(pk=viewer)
	except:
		return False, "Viewer doesn't exist"
	
	try:
		node = node.get_node()
		if node.uploader.id == viewer:
			node.delete(viewer)
			return True, "No error"
		else:
			return False, "You can't delete this node because, you are not the uploader"
	except Exception, err:
		print err
		return False, "Error deleting Node"
		
	
	 
def delete_comment(commentid, userid):
	"""
	Deletes the comment from the node
	"""
	try:
		c = Comment.objects.get(id=commentid)
	except:
		return False, "Comment doesn't exist"
	try:
		p = Person.objects.get(id=userid)
	except:
		return False, "User doesn't exist"
	if p == c.author or p == c.node.get_owner():
		c.delete()
		return True, "No error"
	else:
		return False, "Only comment author and commented node owner can delete comments"

def get_comments(nodeid):
	"""
	Gets all comments for the node
	"""
	try:
		n = Social_node.objects.get(pk=nodeid)
	except:
		return False, "The node doesn't exist"
	comments = Comment.objects.filter(node=n)
	ret =  []
	for c in comments:
		ret.append(c.get_dictionary())
	return ret

def get_all(viewer=None):
	"""
	Returns an array with all the Social_nodes
	"""
	try:
		v=get_person(viewer)
		nodes_mod = Social_node.objects.all()
		nodes = []
		for node in nodes_mod:
			n = node.get_node().get_dictionary(v)
			nodes += [n]
		return nodes
	except:
		return []
	
def get_data(node_id, viewer=None):
	"""
	Returns the details for a node
	"""
	try:
		n = Social_node.objects.get(id=node_id)
		v=get_person(viewer)
		node = n.get_node().get_dictionary(viewer=v)
		return node
	except:
		return None
	


def get_nearby_node(nodeid, radius, viewer):
	"""
	Finds nodes in a radius (in km) from your position
	"""
	try:
		v = get_person(viewer)
		n = Social_node.objects.get(pk=nodeid)
		nodes = Social_node.objects.distance(n.position).order_by("distance").filter(position__distance_lte=(n.position, D(km=float(radius))))
		nds = []
		for node in nodes:
			try:
				n = node.get_node().get_dictionary(v)
				if n["position"]["distance"]:
					nds += [n]
			except:
				pass
		return nds
	except:
		return []
