# Copyright (c) 2008-9 Sociable Marketplaces, Inc. All rights reserved.

from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
import django.contrib.auth.views

urlpatterns = patterns('accounts.views',
    url(r'^$', 'edit', name='account'),
    url(r'^login/$', django.contrib.auth.views.login, name='login'),
    url(r'^logout/$', django.contrib.auth.views.logout, name='logout'),
    url(r'^password/change/$', django.contrib.auth.views.password_change, name='password_change'),
    url(r'^password/change/done/$', django.contrib.auth.views.password_change_done, name='password_change_done'),
    url(r'^password/reset/$', django.contrib.auth.views.password_reset, name='password_reset'),
    url(r'^password/reset/done/$', django.contrib.auth.views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', django.contrib.auth.views.password_reset_confirm),
    url(r'^reset/done/$', django.contrib.auth.views.password_reset_complete),
)
