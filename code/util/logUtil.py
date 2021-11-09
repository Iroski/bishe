import os
import time
import logging
import logging.config
import logging.handlers
from util.ConfigDealer import ConfigDealer
import concurrent_log

class ConsoleFilter(logging.Filter):

    def filter(self, record)     -> bool:
        var = record.levelno >= logging.WARNING or record.levelno == logging.INFO
        return var


def get_log_file_name():
    cur_time = time.strftime("%Y-%m-%d %H-%M", time.localtime())
    path = ConfigDealer.get_log_path()
    if not os.path.exists(path):
        os.makedirs(path)
    return path + cur_time


def init_logger(log_name):
    config = {
        'version': 1,  # 必填项，值只能为1
        'disable_existing_loggers': True,
        # 选填，默认为True，将以向后兼容的方式启用旧行为，此行为是禁用任何现有的非根日志记录器，除非它们或它们的祖先在日志配置中显式命名。如果指定为False，则在进行此调用时存在的记录器将保持启用状态
        'incremental': False,  # 选填，默认为False，作用，为True时，logging完全忽略任何formatters和filters，仅处理handlers的level

        'filters': {
            'consoleFilter': {
                '()': ConsoleFilter
            }
        },
        'formatters':  # 格式器配置专用key，在这里配置formatter，可配置复数formatter
            {
                'myformatter1': {
                    'class': 'logging.Formatter',  # 必填，格式器对应的类
                    'format': '%(asctime)s - %(name)s - [%(levelname)s] - %(message)s',  # fmt格式
                    'datefmt': '%Y-%m-%d %H:%M:%S'
                },
            },

        'handlers':  # 处理器配置专用key，在这里配置handler，可配置复数handler
            {
                'console_handler': {
                    'class': 'logging.StreamHandler',  # 必填，处理器对应的类
                    'level': logging.NOTSET,  # 选填，处理器的日志级别，可填字符串'info'，或者logging.INFO
                    'formatter': 'myformatter1',
                    'filters':['consoleFilter']# 选填，这里要填写formatters字典中的键
                },
                'file_handler': {
                    'class': 'logging.handlers.ConcurrentTimedRotatingFileHandler',  # 必填，处理器对应的类
                    'level': logging.NOTSET,  # 选填，处理器的日志级别，可填字符串'info'，或者logging.INFO
                    'formatter': 'myformatter1',  # 选填，这里要填写formatters字典中的键
                    'filename': log_name + '.log',  # filehandler特有参数，文件名
                    'when': 'H',
                    'delay': True,
                    'backupCount': 2,  # 备份数量
                    'encoding': 'UTF-8',  # 编码格式
                }
            },

        'root':  # 根记录器专用key
            {
                'handlers': ['console_handler', 'file_handler'],  # 列表形式，元素填handlers字典中的handler
                'level': logging.NOTSET,  # 选填，记录器的日志级别，不填则默认Warning级别
            }
    }
    logging.config.dictConfig(config)

