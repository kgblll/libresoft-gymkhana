# -*- coding: utf-8 -*-
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
#    Author : Jose Antonio Santos Cadenas <jcaden __at__ gsyc __dot__ es>
#

from django.template import Context, Library, loader
from django import template

from social.core.api import node 

register = Library()

@register.inclusion_tag("user/raw.xml")
def display_person_xml(person):
    return {"u": person}

@register.simple_tag
def display_search(results, format, prefix=""):
    ret=""
    if prefix!="" and prefix[-1]!="/":
        prefix +="/"

    for element in results:
        print element
        type = element["type"]
        if format=="json":
            ret += u"{\n"
        else:
            ret += u"<%s>" % (type)
        if "person" == type:
            t = loader.get_template("%suser/raw.%s" % (prefix, format))
            ret += u"%s" % t.render(Context({"u": element}))
        elif ("group" == type) or ("dyngroup" == type):
            t = loader.get_template("%sgroup/raw.%s" % (prefix, format))
            ret += u"%s" % t.render(Context({"g": element}))
        elif "note" == type:
            t = loader.get_template("%snote/raw.%s" % (prefix, format))
            ret += u"%s" % t.render(Context({"n": element}))
        elif "photo" == type:
            t = loader.get_template("%sphoto/raw.%s" % (prefix, format))
            ret += u"%s" % t.render(Context({"p": element}))
        elif "sound" == type:
            t = loader.get_template("%ssound/raw.%s" % (prefix, format))
            ret += u"%s" % t.render(Context({"s": element}))
        elif "video" == type:
            t = loader.get_template("%svideo/raw.%s" % (prefix, format))
            ret += u"%s" % t.render(Context({"v": element}))
        else:
            t = loader.get_template("%snodes/raw.%s" % (prefix, format))
            ret += u"%s" % t.render(Context({"n": element}))
        if format=="json":
            ret += u"},\n"
        else:
            ret += u"</%s>" % (type)
    return ret

@register.tag
def comments(parser, token):
    """
    Shows elements created by user_activity in elements variable
    """
    try:
        try:
            tag_name, element_id, format = token.split_contents()
            if not (format[0] == format[-1] and format[0] in ('"', "'")):
                raise template.TemplateSyntaxError, "%r tag's second argument should be in quotes" % tag_name
            return CommentNode(element_id, format[1:-1])
        except ValueError:
            tag_name, element_id = token.split_contents()
            return CommentNode(element_id)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires one or two arguments arguments" % token.contents.split()[0]

class CommentNode(template.Node):
    def __init__(self, element_id, format="xml"):
        self.element_id = template.Variable(element_id)
        self.format = format

    def render(self, context):
        try:
            element_id = self.element_id.resolve(context)
            request = context.get("request")
            if request == None:
                return ""
            else:
                if "comments" in request.GET:
                    template_name = "comments/comments.%s" % self.format
                    t=template.loader.get_template(template_name)
                    data={}
                    data["comments"] = node.get_comments(element_id)
                    rend_context=template.Context(data)
                    return t.render(rend_context)
                else:
                    return ""
        except template.VariableDoesNotExist:
            return ''
        except template.TemplateDoesNotExist:
            try:
                print template_name
            except:
                pass
            return ''
