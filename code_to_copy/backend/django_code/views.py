#!/usr/bin/env python
#-*- coding:utf8 -*-

from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
#--------- 以上几乎是 you_N_G 必用的 



#BEGIN 常用的
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
#END   常用的



# redirect
@require_POST
def post_XXX(request):
    redirect_url = request.META.get('HTTP_REFERER', reverse('XXX', kwargs={XXX}))
    messages.info(request, u'XXX')
    return HttpResponseRedirect(redirect_url)


# set password
from django.contrib.auth.forms import SetPasswordForm
form = SetPasswordForm(data=request.POST or None, user=request.user)


# json response
from django.utils import simplejson as json
return HttpResponse(json.dumps({
        "status": "error_and_show_message",
    }),
    mimetype="application/json"
)


# BEGIN post process single or multi object
def _process_xxx(request, success_msg, fail_msg, process_func):
    redirect_url = request.META.get('HTTP_REFERER', reverse('XXX'))
    pk_list = request.POST.getlist('XXX', [])
    if len(pk_list) != 0:
        for pk in pk_list:
            xxx = get_object_or_404(XXX, pk=pk)
            if xxx_has_not_enought_perm:
                messages.warning(request, fail_msg % xxx)
                return HttpResponseRedirect(redirect_url)
            else:
                process_func(xxx)
        messages.info(request, success_msg)
    else:
        messages.warning(request, u'您什么都没选择')
    return HttpResponseRedirect(redirect_url)


def _process_xxx_func(xxx):
    xxx.publish()

XXX_ACTION_DICT = {
    'xxxAction': {
        'process_func': _process_xxx_func,
        'success_msg': u'xxx成功',
        'fail_msg': u"您没有权限xxx%s，有部分xxxxxx失败",
    },
}


@require_POST
@lock_view_when_post("tree_flow_process_notice")
def process_xxx(request):
    return _process_xxx(request, **XXX_ACTION_DICT[request.POST.get("action")])

''' html
<form action="{% url process_XXX %}" method="POST" style="display:none;">
    {% csrf_token%}
    <input type="hidden" name="XXXids" value="{{XXX.pk}}" />
    <input type="hidden" name="action" value="XXXX" />
    <input type="submit" value="XXX" />
</form>
'''
# END   post process single or multi object


# BEGIN pyEx

#导出
from pyExcelerator import Workbook
import StringIO

wb = Workbook()
sheet = wb.add_sheet(u"XXX")
columns = [u'xxx', u'xxx']
for i, c in enumerate(columns):
    sheet.write(0, i, c)
for i, u in enumerate(XXX, 1):
    sheet.write(i, XXX, XXX)

datafile = StringIO.StringIO()
wb.save(datafile)
datafile.seek(0)
response = HttpResponse(datafile.read(), mimetype='application/vnd.ms-excel')
response['Content-Disposition'] = 'attachment; filename=%s.xls' % urllib.quote_plus((u"%sXXX统计" % XXX).encode('utf8'))
return response

#解析
from pyExcelerator import parse_xls
sheets = parse_xls(upload_file)
sheet_name, sheet_data = sheets[0]
data = sheet_data[(row, col)]

# END pyEx
