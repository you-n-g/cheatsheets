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
# -a archive; -v verbose 

# 利用rsync 拷贝， 同时 exclude 掉一些路径
# rsync -av --exclude='path1/to/exclude' --exclude='path2/to/exclude' source destination
# 这个为什么不行！！！  --exclude-from 也不行？？


# 利用 logrotate 处理log
/path_to_app/log/production.log {
    daily   #按日阶段
    missingok # 如果没找到直接跳过找下一个
    rotate 1000  #保留XXX次
    compress  #压缩
    delaycompress #不压缩前一个(previous)截断的文件（需要与compress一起用）
    dateext  #增加日期作为后缀，不然会是一串无意义的数字
    copytruncate  #清空原有文件，而不是创建一个新文件
}
