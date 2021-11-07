import logging
import threading
from requests.exceptions import RequestException
from exception.exceptions import *

def catch_repo_loader_error(func):
    def wrapper(self, *args, **kwargs):
        logger = logging.getLogger('Loader popular' + threading.current_thread().name[-3:])
        try:
            logger.info("Start: " + self.language)
            func(self, *args, **kwargs)
        except TimeOutException:
            logger.critical("Network time out, please check the internet")
            raise TimeOutException
        except Exception as e:
            logger.critical("System error")
            logger.exception(e)
            raise Exception

    return wrapper