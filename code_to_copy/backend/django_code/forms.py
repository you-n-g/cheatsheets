#!/usr/bin/env python
#-*- coding:utf8 -*-


from django import forms
from models import XXX

class XXXForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(XXXForm, self).__init__(*args, **kwargs)
        #self.fields["XXX"].XXX = XXX
        self.fields["XXX"] = forms.ModelChoiceField(
                queryset=XXX,
                label=u"XXX", empty_label=u"任何XXX", required=False,
        )
    class Meta:
        model = XXX
        fields = ('XXX',)


    def clean_XXX(self):
        raise forms.ValidationError(u"XXX")
        
        return self.cleaned_data
