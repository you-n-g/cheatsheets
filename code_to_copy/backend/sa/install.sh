#!/usr/bin/env bash
# pip
python setup.py build -f #的输出结果最后 的 PIL 1.1.7 SETUP SUMMARY 注意看看依赖是否都满足

# MySQL-python
MySQL-python 的安装需要依赖 libmysqld-dev libmysqlclient-dev...


# PIL
PIL 的安装如果要使用字体，编译的时候必须带入libfreetype
此库在 ubuntu 下叫 libfreetype6-dev
我编译的时候是通过在 setup.py 加入下行解决的。
FREETYPE_ROOT = "/usr/lib/i386-linux-gnu/"

# 快速部署一台ubuntu 服务器
# 0) 配置networks nameserver
# 1)
# 一般机器初始安装的软件 (一般要先update一下)
sudo apt-get install bash-completion dialog memcached python-memcache mercurial build-essential nginx php5-cgi  spawn-fcgi python-django python-imaging python-flup rcconf python-mysqldb screen vim  mysql-server phpmyadmin uwsgi-plugin-python unzip php5 libmysqld-dev python-dev
# 可选  postfix mailutils apache2 libapache2-mod-php5
# 2)
# 配置rc.local
# 3)
# 配置vimrc
# 4)
# 配置phpmyadmin, 配置一下mysql的编码问题








# ====================== for desktop install ============================

# BEGIN xubuntu

# 安装常用软件
sudo apt-get install vim-gnome chromium-browser flashplugin-installer

# 一般会装好 vim插件、workspace 数量，透明度

# 补上窗口在workspace移动的快捷键
Settings - Settings Manager - Window Manager - Keyboard Tab

# 安装Ibus的时候用这个选择默认语言
sudo apt-get install language-selector-gnome

# virtualbox 共享文件夹
sudo mount -t vboxsf virtualbox_shared /shared/
sudo adduser XXXX vboxsf  # 让普通用户成为vboxsf组里的东西，然后用户就可以有权限访问了， 不过这个功能需要用户登出再登录

# 为了能正常访问google的服务
# addd smartladder.googlecode.com/svn/hosts/pc/hosts to hosts

# TODO  14.04 的sunpinyin输入法有问题

# END   xubuntu
