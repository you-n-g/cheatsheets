#!/usr/bin/env python
#-*- coding:utf8 -*-


# BEGIN 对django 1.3适用
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django.core.handlers.wsgi
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
application = django.core.handlers.wsgi.WSGIHandler()
# END   对django 1.3适用
