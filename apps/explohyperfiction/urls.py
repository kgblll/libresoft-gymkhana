# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.defaults import *

# Django settings for server project.
import sys
from os.path import abspath, dirname, join
from os import path


BASEDIR = path.dirname(path.abspath(__file__))
MODIFIED = path.join(BASEDIR,'templates')

from apps.explohyperfiction.rest import views
from apps.explohyperfiction.rest import user
from apps.explohyperfiction.rest import profile
from apps.explohyperfiction.rest import petitions
from apps.explohyperfiction.rest import notices
from apps.explohyperfiction.rest import superuser
from apps.explohyperfiction.rest import events


urlpatterns = patterns('',
    
    #rchivos estáticos
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'apps/explohyperfiction/css'}),
    url(r'^android/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'apps/explohyperfiction/android'}),
    url(r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'apps/explohyperfiction/files'}),
    
    
    #Urls para el home
    url(r'^home/$','apps.explohyperfiction.rest.views.home',),
    url(r'^$', 'apps.explohyperfiction.rest.views.home',), 
    
    url(r'^user/enroll/$', 'apps.explohyperfiction.rest.user.enroll',),
    url(r'^user/unenroll/$', 'apps.explohyperfiction.rest.user.unenroll',),
    url(r'^user/register/$', 'apps.explohyperfiction.rest.user.register',),
    url(r'^user/logout/$','apps.explohyperfiction.rest.user.user_logout',),
    url(r'^user/login/$', 'apps.explohyperfiction.rest.user.user_login',),
    url(r'^user/superuser/$','apps.explohyperfiction.rest.user.superuser',),
    url(r'^user/view/$','apps.explohyperfiction.rest.user.select_view'),
    
    
    url(r'^petitions/$', 'apps.explohyperfiction.rest.petitions.view_petitions',),
    url(r'^petitions/(\d+)/accept/$', 'apps.explohyperfiction.rest.petitions.accept',),
    url(r'^petitions/(\d+)/reject/$', 'apps.explohyperfiction.rest.petitions.reject',),
    
    url(r'^notices/$','apps.explohyperfiction.rest.notices.view',),
    url(r'^notices/(\d+)/delete/$','apps.explohyperfiction.rest.notices.delete',),
    
    url(r'^admin/users/$','apps.explohyperfiction.rest.superuser.view_users',),
    url(r'^admin/user/(\d+)/profile/$','apps.explohyperfiction.rest.superuser.view_user_profile',),
    url(r'^admin/user/(\d+)/delete/$','apps.explohyperfiction.rest.superuser.user_delete',),
    url(r'^admin/user/(\d+)/manager/$','apps.explohyperfiction.rest.superuser.user_manager',),
    url(r'^admin/user/(\d+)/manager/quit/$','apps.explohyperfiction.rest.superuser.user_manager_quit',),
    
    url(r'^admin/groups/$','apps.explohyperfiction.rest.superuser.view_groups',),
    url(r'^admin/groups/delete/(\d+)/$','apps.explohyperfiction.rest.superuser.view_groups_delete',),
    url(r'^admin/groups/profile/(\d+)/$','apps.explohyperfiction.rest.superuser.view_groups_profile',),
    
    url(r'^groups/manager/view/$','apps.explohyperfiction.rest.groups.manager_groups_view',),
    url(r'^groups/manager/create/$','apps.explohyperfiction.rest.groups.manager_create'),
    url(r'^groups/manager/profile/(\d+)/$','apps.explohyperfiction.rest.groups.manager_profile_group',),
    url(r'^groups/manager/delete/(\d+)/$','apps.explohyperfiction.rest.groups.manager_delete_group',),
    url(r'^groups/manager/(\d+)/members/$','apps.explohyperfiction.rest.groups.manager_admin_members',),
    url(r'^groups/manager/petitions/(\d+)/','apps.explohyperfiction.rest.groups.manager_petitions',),
    url(r'^groups/manager/petition/(\d+)/accept/','apps.explohyperfiction.rest.groups.manager_petition_accept',),
    url(r'^groups/manager/petition/(\d+)/reject/','apps.explohyperfiction.rest.groups.manager_petition_reject',),
    
    url(r'^groups/user/view/$','apps.explohyperfiction.rest.groups.user_view',),
    url(r'^groups/user/all/$','apps.explohyperfiction.rest.groups.user_all',),
    url(r'^groups/user/join/(\d+)/$','apps.explohyperfiction.rest.groups.user_join',),
    url(r'^groups/user/delete/(\d+)/$', 'apps.explohyperfiction.rest.groups.user_delete',),
    url(r'^groups/user/profile/(\d+)/$','apps.explohyperfiction.rest.groups.user_group_profile',),
    url(r'^groups/user/request/(\d+)/$','apps.explohyperfiction.rest.groups.user_petition',),
    url(r'^groups/user/request/(\d+)/cancel/$','apps.explohyperfiction.rest.groups.user_petition_quit',),
    
    url(r'^events/manager/create/$','apps.explohyperfiction.rest.events.create',),
    url(r'^events/manager/edit/(\d+)/$', 'apps.explohyperfiction.rest.events.edit',),
    url(r'^events/manager/view/$','apps.explohyperfiction.rest.events.view',),
    url(r'^events/manager/profile/(\d+)/$','apps.explohyperfiction.rest.events.profile',),
    url(r'^events/manager/active/(\d+)/$','apps.explohyperfiction.rest.events.active',),
    url(r'^events/manager/delete/(\d+)/$','apps.explohyperfiction.rest.events.delete',),
    url(r'^events/manager/(\d+)/map/$','apps.explohyperfiction.rest.events.view_map',),
    url(r'^events/manager/print/(\d+)/$','apps.explohyperfiction.rest.views.print_event',),
    
    url(r'^events/manager/(\d+)/questions/$','apps.explohyperfiction.rest.questions.view_questions',),
    url(r'^events/manager/(\d+)/questions/add/$','apps.explohyperfiction.rest.questions.create',),
    
    url(r'^questions/manager/delete/(\d+)/$','apps.explohyperfiction.rest.questions.delete',),
    url(r'^questions/manager/view/(\d+)/$','apps.explohyperfiction.rest.questions.view',),
    url(r'^questions/manager/edit/(\d+)/$','apps.explohyperfiction.rest.questions.edit',), 
    url(r'^questions/manager/print/(\d+)/$','apps.explohyperfiction.rest.views.print_question',),
    
    url(r'^events/user/view/$','apps.explohyperfiction.rest.player.view_events',),
    url(r'^events/user/groups/$','apps.explohyperfiction.rest.player.view_events_by_group',),
    url(r'^events/user/groups/(\d+)/$','apps.explohyperfiction.rest.player.view_events_of_group',),   
    url(r'^events/user/continue/$','apps.explohyperfiction.rest.player.view_events_started'),
    
    url(r'^events/user/start/(\d+)/$', 'apps.explohyperfiction.rest.challenge.start',),
    
    url(r'^challenges/(\d+)/question/(\d+)/$','apps.explohyperfiction.rest.challenge.question',),
    url(r'^challenges/(\d+)/question/(\d+)/answer/(\d+)/$','apps.explohyperfiction.rest.challenge.answer',),
    url(r'^challenges/(\d+)/finish/$','apps.explohyperfiction.rest.challenge.finish',),
    
    url(r'^results/player/(\d+)/$','apps.explohyperfiction.rest.results.view_result_user',),
    url(r'^results/player/$','apps.explohyperfiction.rest.results.user'),
    
    url(r'^results/manager/all/$','apps.explohyperfiction.rest.results.manager_view',),
    url(r'^results/manager/events/$','apps.explohyperfiction.rest.results.manager_events',),
    url(r'^results/player/(\d+)/delete/$','apps.explohyperfiction.rest.results.delete',),
    url(r'^results/manager/events/(\d+)/$','apps.explohyperfiction.rest.results.event_results',),
        
    url(r'^profile/$','apps.explohyperfiction.rest.profile.view_profile',),
    url(r'^profile/petitions/([a-z]*)/$','apps.explohyperfiction.rest.profile.petitions',),
    url(r'^profile/petitions/delete/(.+)/$','apps.explohyperfiction.rest.profile.petitions_delete',),
    url(r'^profile/quit/(.*)/$', 'apps.explohyperfiction.rest.profile.quit',),
    
    url(r'^monitoring/$','apps.explohyperfiction.rest.monitor.main',),
    url(r'^monitoring/(\d+)/$','apps.explohyperfiction.rest.monitor.event',),
    url(r'^monitoring/(\d+)/(\d+)/$','apps.explohyperfiction.rest.monitor.event_challenge',),
    url(r'^api/maps/position/player/(\d+)/$','apps.explohyperfiction.rest.monitor.json_position_player',),
    url(r'^api/maps/position/events/(\d+)/$','apps.explohyperfiction.rest.monitor.json_position_event',),
    url(r'^api/event/(\d+)/results/$','apps.explohyperfiction.rest.monitor.json_event_results',),
    url(r'^api/event/(\d+)/results/(\d+)/$','apps.explohyperfiction.rest.monitor.json_player_results',),

    url(r'^api/json/$','apps.explohyperfiction.rest.api.home',),
    url(r'^api/json/login/$', 'apps.explohyperfiction.rest.api.login',),
    
    url(r'^api/json/events/all/$','apps.explohyperfiction.rest.api.events_all',),
    url(r'^api/json/events/started/$','apps.explohyperfiction.rest.api.events_started',),
    url(r'^api/json/events/profile/(\d+)/$','apps.explohyperfiction.rest.api.event_profile',),
    
    url(r'^api/json/challenge/start/(\d+)/$', 'apps.explohyperfiction.rest.api.challenge_start',),
    url(r'^api/json/challenge/continue/(\d+)/$', 'apps.explohyperfiction.rest.api.challenge_continue',),
    url(r'^api/json/challenge/question/(\d+)/(\d+)/$','apps.explohyperfiction.rest.api.challenge_question',),
    url(r'^api/json/challenge/answer/(\d+)/(\d+)/(\d+)/$','apps.explohyperfiction.rest.api.challenge_answer',),
    url(r'^api/json/challenge/summary/(\d+)/$','apps.explohyperfiction.rest.api.challenge_summary',),
    
    url(r'^api/json/position/$', 'apps.explohyperfiction.rest.api.set_position',),
    
    url(r'^api/json/results/all/$','apps.explohyperfiction.rest.api.results_all',),

    
    
)
