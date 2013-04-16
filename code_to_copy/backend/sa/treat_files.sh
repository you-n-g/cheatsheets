#!/bin/bash

# 使用 7z 压缩
# linux 下 utf8 文件压缩 到 windows 下解压 不乱码
7z a -pPASSWORD OUT_FILE.7z FILE_OR_DIRECTORY
# 注意！！！ 不要用参数 -r ， 这是个坑爹参数！ 如果都是空文件， 解压出来是不会要你输入密码的。。。

cat <<EOF 这是转换文件编码的代码， 因为有的符号在文件名称里不能有
def get_ok_name(unicode_name):
    unicode_name = unicode_name.replace(u' ', u"")
    unicode_name = unicode_name.replace(u'　', u"")
    unicode_name = unicode_name.replace(u'\t', u"")
    unicode_name = unicode_name.replace(u':', u"：")
    unicode_name = unicode_name.replace(u'<', u"《")
    unicode_name = unicode_name.replace(u'>', u"》")
    unicode_name = unicode_name.replace(u'"', u"'")
    unicode_name = unicode_name.replace(u'?', u"？")
    unicode_name = unicode_name.replace(u'/', u"_")
    for ch in '|\:<>"*?':
        unicode_name = unicode_name.replace(ch, "_")
    return unicode_name
EOF


# 下载整站
wget -r -p -np -k http://xxx.com/abc/


# 从一台服务器rsync到另外一台服务器上 "注意 / 不能错!!!" 
rsync  -avz -e ssh /home/deploy/livesites/XXX_SITE  XXX_IP:/home/deploy/livesites/
