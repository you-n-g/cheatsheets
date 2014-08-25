#!/usr/bin/env python
#-*- coding:utf8 -*-

from django.db import models


class XXX(models.Model):
    def __unicode__(self):
        return self

Q = models.Q
F = models.F

XXX = models.CharField(u"XXX", max_length=100)
XXX = models.ForeignKey("XXX", verbose_name=u"XXX", blank=True, null=True, related_name=u'XXX')
XXX = models.IntegerField(u"XXX", default=0)
XXX = models.ManyToManyField(XXX, verbose_name=u"XXX", blank=True, null=True, through=XXX)
XXX = models.BooleanField(u"XXX", default=False)
XXX = models.TextField(u"XXX", blank=True, help_text=u"内容")
create_time = models.DateTimeField(u"创建时间", auto_now_add=True)
update_time = models.DateTimeField(u"最后一次修改时间", auto_now=True)


# 从已有文件读取并保存
from django.core.files.base import File
with open(XXX_PATH) as f:
    XXX.fsfile.save(os.path.basename(XXX_PATH), File(f))
# 尝试一下读取 ImageFile 
# from django.core.files.images import ImageFile


#BEGIN content_type --------------------
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

content_type = models.ForeignKey(ContentType, null=True, blank=True)
object_id = models.PositiveIntegerField(null=True, blank=True)
model_object = generic.GenericForeignKey()

XXX.filter(object_id=XXX.pk, content_type=ContentType.objects.get_for_model(XXX))

XXX_content_type_object.get_all_objects_for_this_type(XXX)
XXX_content_type_object.get_object_for_this_type(XXX)


#END   content_type --------------------



#-------------------- 某些app的用法 --------------------

# BEGIN mptt
org.is_descendant_of(self, include_self=include_self)
org.is_leaf_node()
org.get_children() #得到直属的children
org.get_descendants() #得所有的后代
