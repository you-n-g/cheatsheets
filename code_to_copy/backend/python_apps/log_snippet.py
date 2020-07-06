# BEGIN loguru

# 启动的状态
# https://github.com/Delgan/loguru/issues/51
# 默认add了sys.stderr， id为0
# - 这个在单进程中是会对所有配置生效的。
logger.remove(0)
logger.add("其他的东西")


# 如果你想对logger做一点封装， 又希望代码提示在上层
logger.opt(depth=2).log(level, f"Time {name}: {time.time() - start} s")


# END   loguru


# BEGIN logging

# 机制
# - level: debug info warning error critical, 只显示 大于等于level的logger
#     NOTSET 会从父logger中继承 logging level
#   - 底层不设置level时，会从顶层继承level
# - 每次logger会一级一级往上传递，一直到
#   - 某层propagate=False时停止
#   - 某层level不够，被丢弃了为止(比如 a.b[INFO] 收到debug log之后，是不会传给  a[DEBUG]的)
#      - 先从level判断是否要丢弃，filter是之后的操作； 所以 a.b[level=DEBUG, 加上INFO的filter] 是不会阻止 a[debug]获取消息的 https://stackoverflow.com/a/18059462
# - 同一个logger有多个hanlder，每个handler也可以有自己的logging level

# 设计思路
# 目标：debug某个模块时，可以统一设置Logging的Level;
# - 所以创建logger时最好有模块名称作为前缀
# - 顶层的logger的level更高(要是底层level高也传不过来)

# 默认root logger的 level 一般是 warning, 即只显示 warning error critical
# 默认是输出到 console 中

# 当前logger的状态
# https://pypi.org/project/logging_tree/

# config log; 这个是针对root logger 配置的
import logging
logging.basicConfig(
        filename="XXX.log",
        level=logging.DEBUG,  # be careful that all the subprocess may use the same config
        format='%(asctime)s %(name)s PID:%(process)d [%(levelname)s]:%(message)s', # name 是 logger的name
        # filemode='w', # 加上我就不会append而是覆盖之前的
) # *只有第一次配置会生效，之后就完全无效了*。 因为这个是只针对root设置的。 dictConfig不会有这个问题
# 难点在于当前的系统已经有logger了，如何做到能并存


# 几个比较特殊的 log
LOG.exception("XXX") # level是ERROR， 但是会把 exception的 stack trace 加上，  所以一定要在 exception handler
# 上面的level是ERROR的，如果想要warning带有exception信息，请直接加新参数
# https://stackoverflow.com/a/193153
logger.warning("something raised an exception:", exc_info=True)
# 这个捕捉到的excpetion不是最后触发的exception
# - 捕捉到的是当前层级exception栈中的exception
# - 在某个exception的else或者try中是上一级exception, 只有进入了except中才算下一级


# Add multiple handlers dynamically:
# https://docs.python.org/3/howto/logging-cookbook.html#multiple-handlers-and-formatters
# 动态地制定handler，log名字是动态的


# LOG的组件

# formatters: log的格式

# Handler: 具体的handler，在此设置level, formatter

# logger: logger之间有层级关系，  名字随意取，有从属关系; propagate=True时， message会一直向父节点传;  a是 a.b的parent， 根层级是root(不知对应的名字是"root"还是"")，root logger是必须要设置的;  *主要为了知道message从哪里来的*

# 运行逻辑record首先看当前的Logger的level， 然后过filter， 如果通过，则进入handler阶段，从这个节点逐步向上propagate，调用每层的handler
# - 导致奇怪的逻辑， 在某个父logger的level即使很高，只要它的子logger有级别低的，那么高级别的父logger还是有可能被调用的;  子logger调用后触发的handler和父logger的level无关, 我可以理解为logger的level只控制这一个点的入口(实际有很多入口)，进入之后怎么传播完全看层级关系和handler的level

LOG = logging.getLogger(__file__) # 不加名字或者 只用用 logging的方法 就是用root; logger没有设定level的自动从parent找
# 可以被logger 设置handler， level(TODO: 这个level和 handler的level有什么关系)



# 配置logger 可以使用三种方法
# 1) 上面用函数定义的方法
# 2) 用fileConfig() 定义
# 3) 用dictConfig() 定义
# 描述的信息量都是一样的


# 在这里搜索 https://docs.python.org/3/howto/logging-cookbook.html
# dictConfig 可以找到你要的handler

# 典型的层级
import logging
import logging.config
dictLogConfig = {
    "version": 1,
    "handlers":{
        "consoleHandler": {
            "class":"logging.StreamHandler",
            "formatter":"myFormatter",
        },
        "fileHandler": {
            'class': 'logging.FileHandler',
            'filename': './log/assets.log',
            'mode': 'a',
            'formatter': 'myFormatter',
        },
        # Default file handler for all the warning and error
        "defaultErrFileHandler": {
            'class': 'logging.FileHandler',
            'filename': './log/error.log',
            'mode': 'a',
            'formatter': 'myFormatter',
            "level": "WARNING",
        },
    },
    "loggers":{
        "foo.bar":{
            "handlers":["fileHandler"],
            "level":"INFO",
            "propagate": True,
        },
        "foo":{
            "handlers":["consoleHandler"],
            "level":"INFO",
            "propagate": False,
        },
        "":{
            "handlers":["consoleHandler", "defaultErrFileHandler"],
            "level":"INFO",
        }
    },
    "formatters":{
        "myFormatter":{
            "format":"%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    }
}

# TODO: email handler
config = configparser.ConfigParser()
config.read('config.ini')
# config.ini 中的内容是
# [email]
# mailhost=127.0.0.1
# mailaddr=340448442@qq.com
# subject='Error occurred'

if 'email' in config:
    section = config['email']
    email_handler_template = {
            'class': 'logging.handlers.SMTPHandler',
            'mailhost': section['mailhost'],
            'fromaddr': section['mailaddr'],
            'toaddrs': [section['mailaddr']],
            'subject': section.get('subject', 'Error occurred'),
            'formatter': 'myFormatter',
            "level": "INFO",
        }
    # 系统中的有的信息必须发消息
    # - 一般消息
    # - 没有捕获到的可能导致程序异常退出的信息
    dictLogConfig['handlers']["EmailHandler"] = email_handler_template.copy()
    dictLogConfig['loggers']['email']['handlers'].append('EmailHandler')

    # 系统中所有ERROR级别的log信息必须发消息
    error_handler = email_handler_template.copy()
    error_handler['level'] = 'ERROR'
    dictLogConfig['handlers']["DefaultErrEmailHandler"] = error_handler
    dictLogConfig['loggers']['']['handlers'].append('DefaultErrEmailHandler')

    # 为了信息不重复，所以系统内部会被捕获的异常才log
    # exception，如果会re-raise的异常不log exception
    # 原则： 谁捕获并处理异常谁负责记录; 否则最后一层负责记录。

    # NOTE：最外层要记得捕获 KeyboardInterrupt



logging.config.dictConfig(dictLogConfig)
logger = logging.getLogger("foo.bar")


''' 个人找到最简单的 logger setting
version: 1
handlers:
    consoleHandler:
        class: "logging.StreamHandler"
loggers:
    "":
        level: "INFO"
        handlers:
            - consoleHandler
'''



# Logging之坑！！！！！ NOTE!!!!
# 1) logging坑就坑在新的logger配置不会覆盖旧的logger配置
# 2) 如果 level 是0表示NOTSET,  我这里表现为所有的log都不记录！！！
# 3) 默认dictConfig没有任何handler, 所以即使设置对了 log level， 也不会出消息
#    - basicConfig 似乎没有这个问题

# END   logging
