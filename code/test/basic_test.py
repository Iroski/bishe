from util.DataLoader import start_getting_info
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
# start_getting_info(('Iroski','SE-group-90'))
from util.logUtil import init_logger
import logging
init_logger()
logger = logging.getLogger('logger1')  # 获取配置中的logger对象
    # 输出logger日志记录
logger.info("====================【开始测试】====================")
logger.debug("====================【开始测试】====================")
logger.warning("====================【开始测试】====================")
logger.error("====================【开始测试】====================")
logger.critical("====================【开始测试】====================")
