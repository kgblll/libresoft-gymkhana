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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>._
# 
#    Author : Jorge Fernandez Gonzalez <jorge.fernandez.gonzalez __at__ gmail.com>
#

from django.conf.urls.defaults import *
# Django settings for server project.
import sys
from os.path import abspath, dirname, join
#import deseb
from os import path
from django.views.generic.simple import direct_to_template

BASEDIR = path.dirname(path.abspath(__file__))
MODIFIED = path.join(BASEDIR,'templates')

from apps.gymkhana.rest import views

urlpatterns = patterns('',
    (r'templates/(?P<path>.*)$','django.views.static.serve',{'document_root': 'apps/gymkhana/templates'}),
    (r'img/(?P<path>.*)$','django.views.static.serve',{'document_root': 'apps/gymkhana/img'}),

    (r'^$', 'apps.gymkhana.rest.views.event_list'),
    (r'^overall_standings/show/$', 'apps.gymkhana.rest.views.overall_standings_show'),
    (r'^my_standings/show/$', 'apps.gymkhana.rest.views.my_standings_show'),
    (r'^event/list/$', 'apps.gymkhana.rest.views.event_list'),
    (r'^event/create/$', 'apps.gymkhana.rest.views.event_create'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/show/$', 'apps.gymkhana.rest.views.event_show'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/set_status/$', 'apps.gymkhana.rest.views.event_set_status'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/delete/$', 'apps.gymkhana.rest.views.event_delete'),

    (r'^user/create/$', 'apps.gymkhana.rest.views.user_create'),
    (r'^user/logout/$', 'apps.gymkhana.rest.views.user_logout'),
    (r'^user/login/$', 'apps.gymkhana.rest.views.user_login'),
    (r'^user/list/$', 'apps.gymkhana.rest.views.user_list'),
    (r'^user/(?P<user_id>[1-9][0-9]*)/show/$', 'apps.gymkhana.rest.views.user_show'),
    (r'^user/(?P<user_id>[1-9][0-9]*)/edit/$', 'apps.gymkhana.rest.views.user_edit'),
    (r'^user/(?P<user_id>[1-9][0-9]*)/delete/$', 'apps.gymkhana.rest.views.user_delete'),

    (r'^event/(?P<event_id>[1-9][0-9]*)/message/create/$', 'apps.gymkhana.rest.views.message_create'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/message/list/$', 'apps.gymkhana.rest.views.message_list'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/message/(?P<message_id>[1-9][0-9]*)/reply/$', 'apps.gymkhana.rest.views.message_reply'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/message/(?P<message_id>[1-9][0-9]*)/delete/$', 'apps.gymkhana.rest.views.message_delete'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/message/list/delete/$', 'apps.gymkhana.rest.views.message_list_delete'),

    (r'^event/(?P<event_id>[1-9][0-9]*)/team/team_member/create/$', 'apps.gymkhana.rest.views.team_member_create'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/team/(?P<team_id>[1-9][0-9]*)/team_member/(?P<team_member_id>[1-9][0-9]*)/delete/$', 'apps.gymkhana.rest.views.team_member_delete'),

    (r'^event/(?P<event_id>[1-9][0-9]*)/response/(?P<response_id>[1-9][0-9]*)/edit/$', 'apps.gymkhana.rest.views.response_edit'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/response/(?P<response_id>[1-9][0-9]*)/delete/$', 'apps.gymkhana.rest.views.response_delete'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/response/list/$', 'apps.gymkhana.rest.views.response_list'),

    (r'^event/(?P<event_id>[1-9][0-9]*)/team/list/$', 'apps.gymkhana.rest.views.team_list'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/team/(?P<team_id>[1-9][0-9]*)/show/$', 'apps.gymkhana.rest.views.team_show'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/team/create/$', 'apps.gymkhana.rest.views.team_create'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/team/(?P<team_id>[1-9][0-9]*)/edit/$', 'apps.gymkhana.rest.views.team_edit'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/monitoring/$', 'apps.gymkhana.rest.views.monitoring'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/team/(?P<team_id>[1-9][0-9]*)/information_gymkhana/$', 'apps.gymkhana.rest.views.team_get_information_gymkhana'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/team/(?P<team_id>[1-9][0-9]*)/information_gymkhana/$', 'apps.gymkhana.rest.views.team_get_information_gymkhana'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/team/(?P<team_id>[1-9][0-9]*)/delete/$', 'apps.gymkhana.rest.views.team_delete'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/team/(?P<team_id>[1-9][0-9]*)/message/list_inbox/$', 'apps.gymkhana.rest.views.team_show_inbox_messages'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/team/(?P<team_id>[1-9][0-9]*)/message/list_sent/$', 'apps.gymkhana.rest.views.team_show_sent_messages'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/team/(?P<team_id>[1-9][0-9]*)/message/num_inbox/$', 'apps.gymkhana.rest.views.number_team_inbox_messages'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/team/(?P<team_id>[1-9][0-9]*)/message/num_sent/$', 'apps.gymkhana.rest.views.number_team_sent_messages'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/team/(?P<team_id>[1-9][0-9]*)/skipped_challenge/list/$', 'apps.gymkhana.rest.views.skipped_challenge_list'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/team/join/$', 'apps.gymkhana.rest.views.team_join'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/team/subscribe/$', 'apps.gymkhana.rest.views.team_subscribe'),

    (r'^event/(?P<event_id>[1-9][0-9]*)/team_member/has_team/$', 'apps.gymkhana.rest.views.team_member_has_team'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/team_member/previous_teams/$', 'apps.gymkhana.rest.views.team_member_previous_teams'),

    (r'^event/(?P<event_id>[1-9][0-9]*)/challenge/(?P<challenge_id>[1-9][0-9]*)/delete/$', 'apps.gymkhana.rest.views.challenge_delete'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/challenge/create/$', 'apps.gymkhana.rest.views.challenge_create'),

    (r'^event/(?P<event_id>[1-9][0-9]*)/challenge/(?P<challenge_id>[1-9][0-9]*)/show/$', 'apps.gymkhana.rest.views.challenge_show'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/challenge/(?P<challenge_id>[1-9][0-9]*)/respond/$', 'apps.gymkhana.rest.views.challenge_respond'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/challenge/(?P<challenge_id>[1-9][0-9]*)/skip/$', 'apps.gymkhana.rest.views.challenge_skip'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/challenge/(?P<challenge_id>[1-9][0-9]*)/clue/buy/$', 'apps.gymkhana.rest.views.clue_buy'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/challenge/(?P<challenge_id>[1-9][0-9]*)/clue/show/$', 'apps.gymkhana.rest.views.clue_show'),
    (r'^mobile/menu/$', 'apps.gymkhana.rest.views.mobile_menu'),
    (r'^mobile/login/$', 'apps.gymkhana.rest.views.mobile_login'),
    (r'^mobile/gymkhanas/$', 'apps.gymkhana.rest.views.mobile_gymkhanas'),
    (r'^new_user/$', 'apps.gymkhana.rest.views.new_user'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/list_teams/$', 'apps.gymkhana.rest.views.list_teams'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/team/(?P<team_id>[1-9][0-9]*)/start/$', 'apps.gymkhana.rest.views.start'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/team/(?P<team_id>[1-9][0-9]*)/challenge/(?P<challenge_id>[1-9][0-9]*)/event_show/$', 'apps.gymkhana.rest.views.mobile_event_show'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/team/(?P<team_id>[1-9][0-9]*)/end/$', 'apps.gymkhana.rest.views.end'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/team/(?P<team_id>[1-9][0-9]*)/challenge/(?P<challenge_id>[1-9][0-9]*)/show_list_clues/$', 'apps.gymkhana.rest.views.show_list_clues'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/team/(?P<team_id>[1-9][0-9]*)/challenge/(?P<challenge_id>[1-9][0-9]*)/get_clue/$', 'apps.gymkhana.rest.views.get_clue'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/team/(?P<team_id>[1-9][0-9]*)/challenge/(?P<challenge_id>[1-9][0-9]*)/list_clues/$', 'apps.gymkhana.rest.views.list_clues'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/team/(?P<team_id>[1-9][0-9]*)/finish/$', direct_to_template, {'template': 'dialogs/finish.html'}),
    (r'^event/(?P<event_id>[1-9][0-9]*)/team/(?P<team_id>[1-9][0-9]*)/challenge/(?P<challenge_id>[1-9][0-9]*)/ask_skip/$', 'apps.gymkhana.rest.views.ask_skip'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/team/(?P<team_id>[1-9][0-9]*)/challenge/(?P<challenge_id>[1-9][0-9]*)/skip_list/$', 'apps.gymkhana.rest.views.skip_list'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/team/(?P<team_id>[1-9][0-9]*)/challenge/(?P<challenge_id>[1-9][0-9]*)/skip/$', 'apps.gymkhana.rest.views.skip_challenge'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/team/(?P<team_id>[1-9][0-9]*)/process_message/$', 'apps.gymkhana.rest.views.process_message'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/team/(?P<team_id>[1-9][0-9]*)/show_messages/$', 'apps.gymkhana.rest.views.show_messages'),
    (r'^event/(?P<event_id>[1-9][0-9]*)/team/(?P<team_id>[1-9][0-9]*)/parameters/$', 'apps.gymkhana.rest.views.parameters'),
    (r'^rankings/$', 'apps.gymkhana.rest.views.show_ranking'),
    (r'^logout/$', 'apps.gymkhana.rest.views.mobile_logout'),
)


