# pip
python setup.py build -f #的输出结果最后 的 PIL 1.1.7 SETUP SUMMARY 注意看看依赖是否都满足

# MySQL-python
MySQL-python 的安装需要依赖 libmysqld-dev libmysqlclient-dev...


# PIL
PIL 的安装如果要使用字体，编译的时候必须带入libfreetype
此库在 ubuntu 下叫 libfreetype6-dev
我编译的时候是通过在 setup.py 加入下行解决的。
FREETYPE_ROOT = "/usr/lib/i386-linux-gnu/"
