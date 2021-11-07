import logging
import threading
from requests.exceptions import RequestException
from exception.exceptions import *


def catch_data_loader_error(func):
    def wrapper(self, *args, **kwargs):
        logger = logging.getLogger('Loader ' + threading.current_thread().name[-3:])
        try:
            logger.info("Start: " + self.owner + " " + self.repo)
            result = func(self, *args, **kwargs)
            if result == -3:
                logger.info("Repo: " + self.owner + " " + self.repo + " is up todate")
            else:
                logger.info("Finish repo:" + self.owner + " " + self.repo)
        except DiffException as e:
            logger.debug("Stop work with " + self.owner + " " + self.repo + " ,work with next one")
            pass
        except WebsiteException:
            logger.critical("Internal error, system stop")
            raise WebsiteException
        except TimeOutException:
            logger.critical("Network time out, please check the internet")
            raise TimeOutException
        except Exception as e:
            logger.critical("System error")
            logger.exception(e)
            raise Exception

    return wrapper
