#!/usr/bin/env python
#-*- coding:utf8 -*-

#CKEDITOR
'''
1) 记得拷贝好CKEDITOR 的 static/plugins 的文件
2) 在目标页面加上css
<script type="text/javascript" src="{{STATIC_URL}}/plugins/ckeditor/ckeditor/ckeditor.js"> </script>
3) 设置好settings
4) 在forms中使用 CKEditorWidget
'''
CKEDITOR_MEDIA_PREFIX = "/static/plugins/ckeditor/"
CKEDITOR_UPLOAD_PATH = os.path.join(MEDIA_ROOT, 'ckeditor_uploads/')
CKEDITOR_UPLOAD_PREFIX = os.path.join(MEDIA_URL, "ckeditor_uploads/")
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
        'height': 700,
        'width': 650,
        'language':'zh-cn',
        'pasteFromWordPromptCleanup':True, #Whether to prompt the user about the clean up of content being pasted from MS Word
    },

    'awesome_ckeditor': {
        'toolbar': 'Basic',
    },
}
#CKEDITOR
