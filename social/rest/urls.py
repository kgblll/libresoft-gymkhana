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


from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template
from social.rest.forms import PhotoForm, SoundForm, IconForm, VideoForm, ComparePhotoForm

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', direct_to_template, {"template": "social_test.html", "extra_context":{"photo_form": PhotoForm(), "sound_form": SoundForm(), "icon_form":IconForm(), "video_form":VideoForm(), "compare_form":ComparePhotoForm() }}, name="test"),
    url(r'^test/group/(?P<group>[1-9][0-9]*)/map/$', 'social.rest.test.group_map', name="group_map"),
    url(r'^test/group/map/$', 'social.rest.test.groups_map', name="groups_map"),

    url(r'^user/login/$', 'social.rest.users.user_login', name="user_login"),
    url(r'^user/create/$', 'social.rest.users.user_create_or_modify', name="user_create"),
    url(r'^user/modify/$', 'social.rest.users.user_create_or_modify', {"modify":True}, name="user_modify"),
    url(r'^user/(?P<user>[1-9][0-9]*)/position/$', 'social.rest.users.user_position', name="user_pos_id"),
    url(r'^user/position/$', 'social.rest.users.user_position', name="user_pos"),
    url(r'^user/(?P<user>[1-9][0-9]*)/data/$', 'social.rest.users.user_data', name="user_data_id"),
    url(r'^user/data/$', 'social.rest.users.user_my_data', name="user_data"),
    url(r'^user/(?P<user>[1-9][0-9]*)/friends/$', 'social.rest.users.user_friends', name="user_friends"),
    url(r'^user/friends/$', 'social.rest.users.user_friends', name="user_my_friends"),
    url(r'^user/(?P<user>[1-9][0-9]*)/friendship_invitations/$', 'social.rest.users.user_friendship_invitations', name="user_friendship_invitation"),
    url(r'^user/friendship_invitations/$', 'social.rest.users.user_friendship_invitations', name="user_my_friendship_invitations"),
    url(r'^user/(?P<user>[1-9][0-9]*)/near_people/$', 'social.rest.users.user_near', name="user_near"),
    url(r'^user/near_people/$', 'social.rest.users.user_near', name="user_near_own"),
    url(r'^user/near_friends/$', 'social.rest.users.user_near_friends', name="user_near_friends"),
    url(r'^user/(?P<user>[1-9][0-9]*)/set_status/$', 'social.rest.users.user_set_status', name="user_set_status_id"),
    url(r'^user/set_status/$', 'social.rest.users.user_set_status', name="user_set_status"),
    url(r'^user/set_avatar/$', 'social.rest.users.user_set_avatar', name="user_set_avatar"),
    url(r'^user/list/$', 'social.rest.users.user_all', name="user_all"),
    url(r'^user/delete/$', 'social.rest.users.user_delete', name="user_delete"),
    url(r'^user/relation/$', 'social.rest.users.user_relation', name="user_relation"),
    url(r'^user/relation/delete/$', 'social.rest.users.user_relation_delete', name="user_relation_delete"),
    url(r'^user/groups/$', 'social.rest.users.user_groups', name="user_groups"),
    url(r'^user/privacy/status/$', 'social.rest.privacy.privacy', name="privacy"),
	url(r'^user/privacy/change/$', 'social.rest.privacy.change_privacy', name="change_privacy"),


    url(r'^node/(?P<node_id>[1-9][0-9]*)/position_update/$', 'social.rest.nodes.node_set_position', name="node_set_position"),
    url(r'^node/(?P<node_id>[1-9][0-9]*)/tag/$', 'social.rest.nodes.node_tag', name="node_tag"),
    url(r'^node/(?P<node_id>[1-9][0-9]*)/untag/$', 'social.rest.nodes.node_untag', name="node_untag"),
    url(r'^node/(?P<node_id>[1-9][0-9]*)/comment/$', 'social.rest.nodes.node_comment', name="node_comment"),
    url(r'^node/comment/delete/$', 'social.rest.nodes.node_delete_comment', name="node_delete_comment"),
    url(r'^node/(?P<node_id>[1-9][0-9]*)/privacy/status/$', 'social.rest.privacy.privacy', name="node_privacy"),
    url(r'^node/(?P<node_id>[1-9][0-9]*)/privacy/change/$', 'social.rest.privacy.change_privacy', name="node_change_privacy"),
	url(r'^node/(?P<node_id>[1-9][0-9]*)/layers/$', 'social.rest.views.node_get_layers', name="node_get_layers"),

    
    
	url(r'^group/list/$', 'social.rest.groups.group_list', name="group_list"),
    url(r'^group/create/$', 'social.rest.groups.group_create', name="group_create"),
    url(r'^group/(?P<group>[1-9][0-9]*)/data/$', 'social.rest.groups.group_data', name="group_data"),
    url(r'^group/(?P<group>[1-9][0-9]*)/elements/$', 'social.rest.groups.group_elements', name="group_elements"),
    url(r'^group/delete/$', 'social.rest.groups.group_delete', name="group_delete"),
    url(r'^group/join/$', 'social.rest.groups.group_join', name="group_join"),
    url(r'^group/join/delete/$', 'social.rest.groups.group_join_delete', name="group_unjoin"),


	url(r'^layer/(?P<layer_id>(.*))/node/(?P<node_id>[1-9][0-9]*)/update_avaliable_dates/$', 'social.rest.views.node_set_dates', name="node_set_dates"),
	url(r'^layer/(?P<layer_id>(.*))/node/(?P<node_id>[1-9][0-9]*)/delete/$', 'social.rest.views.node_delete', name="node_delete"),
	url(r'^layer/(?P<layer_id>(.*))/note/upload/$', 'social.rest.notes.note_upload', name="note_upload"),
	url(r'^layer/(?P<layer_id>(.*))/photo/upload/$', 'social.rest.photos.photo_upload', name="photo_upload"),
    url(r'^layer/(?P<layer_id>(.*))/sound/upload/$', 'social.rest.sounds.sound_upload', name="sound_upload"),
    url(r'^layer/(?P<layer_id>(.*))/video/upload/$', 'social.rest.videos.video_upload', name="video_upload"),

    url(r'^layer/(?P<layer_id>(.*))/node/(?P<node_id>[1-9][0-9]*)/sound_file/$', 'social.rest.views.node_sound_file', name="node_sound_file"),
    url(r'^layer/(?P<layer_id>(.*))/node/(?P<node_id>[1-9][0-9]*)/video_file/$', 'social.rest.views.node_video_file', name="node_video_file"),

	url(r'^layer/(?P<layer_id>(.*))/node/(?P<node_id>[1-9][0-9]*)/image/$', 'social.rest.views.node_image', name="node_image"),
	url(r'^layer/(?P<layer_id>(.*))/node/(?P<node_id>[1-9][0-9]*)/image/thumb/$', 'social.rest.views.node_image', {"thumb": True}, name="node_image_thumb"),
	url(r'^layer/(?P<layer_id>(.*))/node/(?P<node_id>[1-9][0-9]*)/image/large/$', 'social.rest.views.node_image', {"size": "large"}, name="node_image_large"),
	url(r'^layer/(?P<layer_id>(.*))/node/(?P<node_id>[1-9][0-9]*)/image/medium/$', 'social.rest.views.node_image', {"size": "medium"}, name="node_image_medium"),
	url(r'^layer/(?P<layer_id>(.*))/node/(?P<node_id>[1-9][0-9]*)/image/small/$', 'social.rest.views.node_image', {"size": "small"}, name="node_image_small"),
    

	url(r'^layer/(?P<layer_id>(.*))/node/(?P<node_id>[1-9][0-9]*)/data/$', 'social.rest.views.node_data', name="node_data"),
    
	
    url(r'^layer/(?P<layer_id>(.*))/search/$', 'social.rest.layers.request_layer', name="request_layer"),
    url(r'^layer/(?P<layer_id>(.*))/info/$', 'social.rest.layers.info_layer', name="info_layer"),
    url(r'^layer/(?P<layer_id>(.*))/icon/$', 'social.rest.layers.icon_layer', name="icon_layer"),
    url(r'^layer/(?P<layer_id>(.*))/change_icon/$', 'social.rest.layers.icon_change_layer', name="icon_change_layer"),
    url(r'^layer/(?P<layer_id>(.*))/categories/$', 'social.rest.layers.categories_layer', name="categories_layer"),
    url(r'^layer/(?P<layer_id>(.*))/delete/$', 'social.rest.layers.delete_layer', name="delete_layer"),
    url(r'^layer/(?P<node_id>[1-9][0-9]*)/privacy/status/$', 'social.rest.privacy.privacy', name="privacy"),
    url(r'^layer/(?P<node_id>[1-9][0-9]*)/privacy/change/$', 'social.rest.privacy.change_privacy', name="change_privacy"),
    url(r'^layer/list/$', 'social.rest.layers.list_layer', name="list_layer"),
    url(r'^layer/create/$', 'social.rest.layers.create_layer', name="create_layer"),

	url(r'^layer/query/multi-search/$', 'social.rest.layers.request_layer', {"multi_search": True}, name="request_layer"),

    url(r'^privacy/roles/$', 'social.rest.privacy.get_roles', name="roles"),
    url(r'^privacy/permissions/$', 'social.rest.privacy.get_permissions', name="permissions"),
)
