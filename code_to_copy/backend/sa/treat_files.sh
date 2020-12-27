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
# The default maximum depth is 5
# -l depth
# -r 表示递归下载， 但是一般得配上 -np表示只递归下载本站链接
# -k 表示将连接改为本地链接
# -p 表示获得网页显示所需要的元素


# 从一台服务器rsync到另外一台服务器上 "注意 / 不能错!!!":  如果source不以/结尾， 那么会当成一个新文件放进去；否则会把source和target这两个文件夹同步成一样的。
# 第一个"/"是关键(关系这个路径是当成文件还是文件夹)，第二个"/"可能无关紧要
rsync  -avzrP -e ssh /home/deploy/livesites/XXX_SITE  XXX_IP:/home/deploy/livesites/
# -a archive; -v verbose; -z compress; -r recursive; -P progress
# 对小文件, -a 会加速很多(不依赖z来压缩); 这个命令可以多次运行，每次只传输两个文件之间的差
# 网速好不要用 -z
# -p 可以保留用户id，但是用户的映射关系用的名字，--numeric-ids 这个参数应该可以强制用用户数字id来rynsc(而且)

# 利用rsync 拷贝， 同时 exclude 掉一些路径
# rsync -av --exclude='path1/to/exclude' --exclude='path2/to/exclude' source destination
# --exclude-from 代表从指定文件里读取exclude的list:
#   - 注意里面要写的是pattern，看起来像wildcard
# 下面这个说明非常详细
# https://linoxide.com/linux-how-to/linux-rsync-examples-exclude-files-directories/
# - rsync的 --include-from 比你想象中的更复杂: https://askubuntu.com/a/558830
#   - 估计坑在:  相对路径 & += 是必须了解的
#   - 建议用 --files-from

# 坑: 
# - exclude总是会用相对路径执行
# - 如果用jump host 来代理加速拷贝文件， 有时候速度会变慢; 通过jump host 做端口转发，再scp  127.0.0.1 能速度正常

# rsync不会删除文件！！！！  需要加入 --delete这种参数
# 如果希望能不覆盖新的文件，可以用 --ignore-existing



# 上面的命令有点类似下面的命令，但是下面更灵活；比如可以将一个机器下的压缩包cat到另外一个机器上解压。
tar czf - stuff_to_backup | ssh backupmachine tar xvzf -



# https://stackoverflow.com/questions/18731603/how-to-tar-certain-file-types-in-all-subdirectories
find ./someDir -name "*.php" -o -name "*.html" | tar -cf my_archive -T -
# -T 表示分割文件名字的方式


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
