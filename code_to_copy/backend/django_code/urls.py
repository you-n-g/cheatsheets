#!/usr/bin/env python
#-*- coding:utf8 -*-
from django.conf.urls.defaults import patterns, url, include

from django.views.generic.simple import direct_to_template

urlpatterns = patterns('XXX.views',
    url(r'^XXX/(?P<pid>\d+)/$', 'XXX', name='XXX'),
    url(r'^XXX/', include('XXX.XXX.urls')),
    url(r"^XXX/$", u"django.contrib.auth.views.login", {
                                'template_name': 'registration/login.html',
                                #'authentication_form': XXX_AUTH_FORM,
        }),
    ('^XXX/$', direct_to_template, {'template': 'XXX.html'})
)
