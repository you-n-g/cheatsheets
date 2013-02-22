#!/usr/bin/env python
#-*- coding:utf8 -*-

from django.db import models


class XXX(models.Model):
    def __uniocode__(self):
        return self

Q = models.Q
F = models.F

XXX = models.CharField(u"XXX", max_length=100)
XXX = models.ForeignKey("XXX", verbose_name = u"XXX", blank = True, null = True, related_name = u'XXX')
XXX = models.IntegerField(u"XXX", default = 0)
XXX = models.ManyToManyField(XXX, verbose_name = u"XXX", blank = True, null = True, through = XXX)
XXX = models.BooleanField(u"XXX", default = False)
XXX = models.TextField(u"XXX", blank=True, help_text=u"内容")
create_time = models.DateTimeField(u"创建时间", auto_now_add=True)
publish_time= models.DateTimeField(u"最后一次修改时间", auto_now = True)
