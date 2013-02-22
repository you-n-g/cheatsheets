#!/usr/bin/env python
#-*- coding:utf8 -*-

from django import forms
from models import XXX

class XXXForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NoticeForm, self).__init__(*args, **kwargs)
        #self.fields["XXX"].XXX = XXX
    class Meta:
        model = XXX
        fields = ('XXX',)

#BEGIN CKEDITOR
from ckeditor.widgets import CKEditorWidget
self.fields["XXX"].widget = CKEditorWidget()
#END   CKEDITOR
