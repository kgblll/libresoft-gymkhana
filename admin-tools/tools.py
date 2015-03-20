#!/usr/bin/python

def del_photos(field, start):
    from social.core.models import Photo
    e = "Photo.objects.filter(%s__startswith='%s')" % (field, start)
    list = eval (e)
    for x in list:
        x.delete()


