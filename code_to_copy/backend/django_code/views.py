#!/usr/bin/env python
#-*- coding:utf8 -*-

#BEGIN 常用的
from django.http import HttpResponseForbidden
#END   常用的



from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.contrib import messages

# redirect
@require_POST
def post_XXX(request):
    redirect_url = request.META.get('HTTP_REFERER', reverse('XXX', kwargs = {XXX}))
    messages.info(request, u'XXX')
    return HttpResponseRedirect(redirect_url)


# set password 
from django.contrib.auth.forms import SetPasswordForm
form = SetPasswordForm(data = request.POST or None, user = request.user)


# json response
from django.utils import simplejson as json
return HttpResponse(json.dumps({
        "status": "error_and_show_message",
    }),
    mimetype="application/json"
)
