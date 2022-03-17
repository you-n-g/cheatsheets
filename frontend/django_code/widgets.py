#!/usr/bin/env python
#-*- coding:utf8 -*-

from django.conf import settings

from django.forms.widgets import XXXWidget

class XXXInput(XXXWidget):
    class Media:
        js = ('%sXXX' % settings.STATIC_URL, )
        css = {
             'all': ('%sXXX' % settings.STATIC_URL,)
        }
