#
#  Copyright (C) 2010 GSyC/LibreSoft, Universidad Rey Juan Carlos
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
#    Author : Roberto Calvo Palomino <rocapal_at_librsoft_dot_es>        
#

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
from django.template import Context
from social.layers.layers_manager import *
from social.rest.layers import create_layer, delete_layer, request_layer
from social.rest.notes import note_upload
from social.rest.photos import photo_upload
from social.rest.sounds import sound_upload
from social.rest.views import node_delete

from social.core.api_layer import get_layer

def init (request):

    con = Context({ 'mensaje'   : 'hola', })

    html = render_to_response ( 'backend/login/index.html', con )
    return HttpResponse( html)


def login(request):
    
    if request.method == 'POST':
        password =  request.POST.get('password', '')
        username =  request.POST.get('username', '')
        
        user = auth.authenticate( username=username , password=password)
        
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/backend/home')
        else:
            con =  Context({ 'message' : "Error de autenticacion" , })
            return render_to_response('backend/login/', con )
        
    html = render_to_response ('backend/login/index.html')
    return HttpResponse( html)

        
def home (request):
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect('backend/login/')
    
    html = render_to_response ('backend/home.html')
    return HttpResponse( html)


def layers (request):
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect('backend/layers/')    
    
    msg = ""
    
    if request.method == 'POST':
        data = create_layer(request)
    
    success, results = layers_list (request.user,True)
    
    
    con =  Context({ 'url_create_layer': '/backend/layers/',
                     'results' : results ,
                     'msg' : msg })
    
    html = render_to_response ('backend/layers.html', con )
    return HttpResponse( html)

def get_layers_content (request, layer_id):
    
    options = request.GET.copy()
    options["user"] = request.user
    options["layer_id"] = layer_id
    options["latitude"]=0.0
    options["longitude"]=0.0
    options["radius"]=0.0
    options["category"]="0"
    options["elems"]=10000
    
    success, response = layers_search(layer_id, "", options)
   
    print response
    print type (response[0].position)
    
    con =  Context({ 'url_create_layer': '/backend/layers/',
                     'list' : response,
                     'layer_id' : layer_id,
                     'msg' : "" })
    
    html = render_to_response ('backend/node_list.html', con )
    return HttpResponse( html)
    
def layers_delete (request):
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/backend/layers/') 
    
    
    if request.method == 'POST':
        
        idInt = int(request.POST["id"])
        res = delete_layer(request,idInt)
    
    return HttpResponseRedirect('/backend/layers/') 
    
    
        
def contents (request):
    
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect('backend/contents/')    
    
    success, results = layers_list (request.user,True)          
    
    msg=""
    con =  Context({ 'results' : results ,
                     'msg' : msg })
    html = render_to_response ('backend/contents.html', con )
    return HttpResponse(html)


def list_nodes (request):
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect('backend/contents/')
    
    con =  Context({ 'layer' : layer ,
                     'msg' : msg })
    
    html = render_to_response ('backend/contents.html', con )
    return HttpResponse(html)
    
def delete_node (request, layer_id, node_id):
    
    result = node_delete(request,layer_id,node_id)
    print result
    
    return get_layers_content(request, layer_id)
    
def note_create (request):
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect('backend/contents/')
    
    res = note_upload(request, int(request.POST["layer"]) )
    success, results = layers_list (request.user,True)          
    
    print res
    
    msg=""
    con =  Context({ 'results' : results ,
                     'msg' : msg })
    html = render_to_response ('backend/contents.html', con )
    return HttpResponse(html)

    
def photo_create (request):
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect('backend/contents/')
    
    res = photo_upload(request, int(request.POST["layer"]) )
    success, results = layers_list (request.user,True)          
    
    print res
    
    msg=""
    con =  Context({ 'results' : results ,
                     'msg' : msg })
    html = render_to_response ('backend/contents.html', con )
    return HttpResponse(html)


def sound_create (request):
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect('backend/contents/')
    
    res = sound_upload(request, int(request.POST["layer"]) )
    success, results = layers_list (request.user,True)          
    
    print res
    
    msg=""
    con =  Context({ 'results' : results ,
                     'msg' : msg })
    html = render_to_response ('backend/contents.html', con )
    return HttpResponse(html)    