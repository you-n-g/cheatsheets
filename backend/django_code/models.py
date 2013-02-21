#!/usr/bin/env python
#-*- coding:utf8 -*-

from django.db import models


class XXX(models.Model):
    def __uniocode__(self):
        return self

Q = models.Q
F = models.F

XXX = models.CharField(u"XXX", max_length=100)
XXX = models.ForeignKey('XXX', verbose_name = u"XXX", blank = True, null = True, related_name = u'XXX')
