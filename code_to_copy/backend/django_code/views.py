#!/usr/bin/env python
#-*- coding:utf8 -*-




from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.contrib import messages

@require_POST
def post_XXX(request):
    redirect_url = request.META.get('HTTP_REFERER', reverse('XXX', kwargs = {XXX}))
    messages.info(request, u'XXX')
    return HttpResponseRedirect(redirect_url)
