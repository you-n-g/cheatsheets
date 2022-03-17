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
# - 可以理解为有  入口层   处理层(包含了传播层)
#   - 入口层:  logging.Logger
#       - logging.Logger.isEnabledFor 把关 判断
#       - 只管信息会不会进入下面层 (handle函数)
#       - 先经过filter把关(注意filter)， 然后就进入 logging.Logger.callHandlers 进入处理层
#   - 进入处理层后和上层就没有关系了,  核心代码在logging.Logger.callHandlers
#       - 一边处理一边传播
#           - 注意这里处理的时候就直接调用handler(s)的handle了(而不是调用Logger.handle)
#           - 传播的过程完全由 propagate 控制(不收level, filter的影响)
# 其他零碎的组件:
# - formatters: log的格式, 用于 Handler 中

# 一些注意的点
# - NOTSET 会从父logger中继承 logging level(底层不设置level时，会从顶层继承level)
# - Logger 和 Handler都是有自己的filter类:  别搞混了
# - 默认root logger的 level 一般是 warning, 即只显示 warning error critical
#   默认是输出到 console 中
# - 入口层的filter，level不会影响到 处理层 !!!

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
