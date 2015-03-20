# -*- coding: UTF-8 -*-

from urllib2 import urlopen
from xml.dom.minidom import parseString
from django.template import Template, Context
from format.utils import  getResponseFormat, generateResponse
from commons.utils import getInnerText

import json

import sys
import site

class ItemContent(object):
  def __init__(self):
   self.title = ""
   self.summary = ""
   self.date = ""
   self.latitude = ""
   self.longitude = ""
   self.url = ""
   self.service = ""
   self.credits = ""
   self.keywords = ""
   self.img = "no"
   self.img_width = ""
   self.img_height = ""
   self.img_url = ""
   self.thumb = "no"
   self.thumb_width = ""
   self.thumb_height = ""
   self.thumb_url = ""
   self.place = "no"
   self.place_address = ""
   self.place_phone = ""
   self.place_postalcode = ""
   self.place_country = ""
   self.place_region = ""
   self.place_city = ""
   self.video = "no"
   self.video_link = ""
   self.video_format = ""

def get_11870_content( latitud, longitud, radio, texto ):

   url11870 = "http://11870.com/api/v1/search?lat=%s&lon=%s&radius=%s&authSign=3572a8bb3f7dc6c9b2b80907beff2f5f&appToken=74805753bf8cef647b46101266370e05&q=%s" % ( latitud, longitud, radio, texto )
   r = urlopen(url11870)
   s11870 = r.read()
   dom = parseString(s11870)
   feed11870 = dom.firstChild

   resp = feed11870.toxml();

   items_11870 = []
   for item in feed11870.getElementsByTagName("entry"):
     item_11870 = ItemContent()

     item_11870.service = "11870"
     item_11870.place = "yes"

     item_11870.title = getInnerText(item, "title")
     item_11870.summary = getInnerText(item, "summary")
     item_11870.url = getInnerText(item, "id")
     item_11870.place_address = getInnerText(item, "oos:useraddress")
     item_11870.place_phone = getInnerText(item, "oos:telephone")
     item_11870.place_city = getInnerText(item, "oos:locality")
     item_11870.place_region = getInnerText(item, "oos:subadministrativearea")
     item_11870.place_country = getInnerText(item, "oos:country")

     # este codigo absurdo es necesario para serializar en formato json
     item_11870.title = item_11870.title.replace( "a", "a" )

     pos = getInnerText(item, "gml:pos")
     item_11870.latitude = pos.split(' ')[0]
     item_11870.longitude = pos.split(' ')[1]

     items_11870.append(item_11870);

   return items_11870

def get_panoramio_content( latitud, longitud, radio, texto ):

    # got operations below from http://assets.en.oreilly.com/1/event/2/Geo%20Distance%20Search%20with%20MySQL%20Presentation.ppt
    # 1 miles = 1.609344 kilometers

    miny = float(latitud) - ( float(radio) / ( 69 * 1.609344 ) )
    maxy = float(latitud) + ( float(radio) / ( 69 * 1.609344 ) )

    # estos son los calculos correctos pero python da error en las funciones cos y radians
    #minx = float(longitud) - float(radio) / ( abs( cos( radians( float(latitud) ) * (69 * 1.609344) )))
    #maxx = float(longitud) + float(radio) / ( abs( cos( radians( float(latitud) ) * (69 * 1.609344) )))

    # chapuza para obtener un rango alrededor de la longitud dada
    minx = float(longitud) - ( float(radio) / ( 69 * 1.609344 ) * 1 )
    maxx = float(longitud) + ( float(radio) / ( 69 * 1.609344 ) * 1 )

    # la chapuza de arriba genera un rectangulo mas pequenyo de lo que deberia
    # python: latitud 40.333313 miny 40.3261086963 maxy 40.3405173037 longitud -3.87429 minx -3.88149430368 maxx -3.86708569632
    # perl: latitud 40.333313 longitud -3.87429 - minx -4.37429 maxx -3.33800323823823 - pi 3.14159265358979 - degrees 0.703949110087432
    #print "latitud %s miny %s maxy %s longitud %s minx %s maxx %s" % ( latitud, miny, maxy, longitud, minx, maxx )

    urlpanoramio = "http://www.panoramio.com/map/get_panoramas.php?order=popularity&set=public&from=0&to=10&size=small&minx=%s&miny=%s&maxx=%s&maxy=%s" % ( minx, miny, maxx, maxy )
    r = urlopen(urlpanoramio)
    spanoramio = r.read()
    feedpanoramio = json.JsonReader().read(spanoramio)

    items_panoramio = []
    for item in feedpanoramio["photos"]:
      item_panoramio = ItemContent()

      item_panoramio.service = "panoramio"
      item_panoramio.img = "yes"
      item_panoramio.thumb = "yes"
      item_panoramio.credits = "yes"

      item_panoramio.title = unicode(item["photo_title"], 'UTF-8')
      #item_panoramio.id = item["photo_id"]
      item_panoramio.date = unicode(item["upload_date"], 'UTF-8')
      item_panoramio.longitude = item["longitude"]
      item_panoramio.img_url = item["photo_file_url"]
      item_panoramio.img_height = item["height"]
      item_panoramio.img_width = item["width"]
      item_panoramio.thumb_url = item["photo_file_url"].replace('/small/','/thumbnail/')
      item_panoramio.thumb_height = int( int(item["height"]) / 2.4 )
      item_panoramio.thumb_width = int( int(item["width"]) / 2.4 )
      item_panoramio.latitude = item["latitude"]
      item_panoramio.credits_owner = unicode(item["owner_name"], 'UTF-8')
      item_panoramio.credits_url = item["owner_url"]
      item_panoramio.url = item["photo_url"]

      items_panoramio.append(item_panoramio);

    return items_panoramio

def join_rss_content(request):

    # valores por defecto de parametros

    tipo = ""
    latitud = ""
    longitud = ""
    radio = 0;
    texto = ""
    format = "XML"

    if request.method == 'GET':

      if "tipo"     in request.GET: tipo=request.GET['tipo']
      if "latitud"  in request.GET: latitud=request.GET['latitud']
      if "longitud" in request.GET: longitud=request.GET['longitud']
      if "radio"    in request.GET: radio=request.GET['radio']
      if "texto"    in request.GET: texto=request.GET['texto']
      if "format"   in request.GET: format=request.GET['format']

    if request.method == 'POST':

      if "tipo"     in request.POST: tipo=request.POST['tipo']
      if "latitud"  in request.POST: latitud=request.POST['latitud']
      if "longitud" in request.POST: longitud=request.POST['longitud']
      if "radio"    in request.POST: radio=request.POST['radio']
      if "texto"    in request.POST: texto=request.POST['texto']
      if "format"   in request.POST: format=request.POST['format']

    if tipo == "":
      data = {'code' : '500', 'description' : 'Missing parameter tipo' }
      return generateResponse(format, data, "error")

    if latitud == "":
      data = {'code' : '500', 'description' : 'Missing parameter latitud' }
      return generateResponse(format, data, "error")

    if longitud == "":
      data = {'code' : '500', 'description' : 'Missing parameter longitud' }
      return generateResponse(format, data, "error")

    if radio == 0:
      data = {'code' : '500', 'description' : 'Missing parameter radio' }
      return generateResponse(format, data, "error")

    if not (format == "XML") and not (format == "JSON"):
      data = {'code' : '500', 'description' : 'format parameter must be XML, JSON or blank defaulting to xml' }
      return generateResponse(format, data, "error")

    items_content = []

    if (tipo == "all") or (tipo == "11870") or (tipo == "place"):
     items_11870 = get_11870_content( latitud, longitud, radio, texto )
     items_content.extend(items_11870)

    if (tipo == "all") or (tipo == "panoramio") or (tipo == "img"):
     items_panoramio = get_panoramio_content( latitud, longitud, radio, texto )
     items_content.extend(items_panoramio)

    if format == "JSON":  # tenemos que generar una estructura serializable para json

      items_content_json = []

      # generar una estructura serializable
      for item in items_content:

        item_json = { }

        item_json[ "title"     ] = item.title
        item_json[ "date"      ] = item.date
        item_json[ "url"       ] = item.url
        item_json[ "summary"   ] = item.summary
        item_json[ "longitude" ] = item.longitude
        item_json[ "latitude"  ] = item.latitude
        item_json[ "service"   ] = item.service
        item_json[ "keywords"  ] = item.keywords

        item_json[ "img"   ] = item.img
        if item.img == "yes":
          item_json[ "img_width"  ] = item.img_width
          item_json[ "img_height" ] = item.img_height
          item_json[ "img_url"    ] = item.img_url

        item_json[ "thumb" ] = item.thumb
        if item.thumb == "yes":
          item_json[ "thumb_width"  ] = item.thumb_width
          item_json[ "thumb_height" ] = item.thumb_height
          item_json[ "thumb_url"    ] = item.thumb_url

        item_json[ "place" ] = item.place
        if item.place == "yes":
          item_json[ "place_address"    ] = item.place_address
          item_json[ "place_phone"      ] = item.place_phone
          item_json[ "place_postalcode" ] = item.place_postalcode
          item_json[ "place_country"    ] = item.place_country
          item_json[ "place_region"     ] = item.place_region
          item_json[ "place_city"       ] = item.place_city

        item_json[ "video" ] = item.video
        if item.video == "yes":
          item_json[ "video_link"    ] = item.video_link
          item_json[ "video_format"  ] = item.video_format

        item_json[ "credits" ] = item.credits
        if item.credits == "yes":
          item_json[ "credits_owner" ] = item.credits_owner
          item_json[ "credits_url"   ] = item.credits_url

        items_content_json.append(item_json)

      return generateResponse(format, {'resources': items_content_json}, "webservices")

    else:

      return generateResponse(format, {'items_content': items_content}, "webservices")
 
