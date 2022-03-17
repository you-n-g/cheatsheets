""" 下面这个config可以直接安装特定分支的qlib
install_requires=[
    'pyqlib>=0.7.2',
]
dependency_links=["https://github.com/microsoft/qlib/tarball/neutrader#egg=pyqlib-0.8.0.100"],
# 其中 `#egg=pyqlib-0.8.0.100` 作为索引; 最后安装的版本号(`pip freeze`) 是根据最后下载的 tarball来
# dependency_links 的关键是它得指向一个 tarball https://stackoverflow.com/a/32689886
"""

# 下面是更正规的写法:  上面的写法会导致 `pip install -e .` 出错;
install_requires = ["pyqlib @ https://github.com/microsoft/qlib/tarball/neutrader#egg=pyqlib-0.8.0.99"]



# Tips
# 尽量避免使用 `python setup.py develop`, 而是使用 `pip install -e .` :  https://stackoverflow.com/q/30306099
# - 有个问题的是 setup.py develop 会装你的dependancy的 pre-release 版本，有的时候会装到一些不是很稳定的依赖
# - `pip install -e .` 不同点
#   - egg-info 是相对你项目的路径
#   - 使用wheel安装 ?
#   - 安装dependancies是使用 pip ， 而不是 easy_install


