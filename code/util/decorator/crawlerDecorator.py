import logging
import threading
from requests.exceptions import RequestException
from exception.exceptions import *


def catch_validation_error(func):
    def wrapper(self, times=0, *args, **kwargs):
        logger = logging.getLogger('Validation ' + threading.current_thread().name[-3:])
        try:
            result = func(self, *args, **kwargs)
            if type(result) == str:
                if result == "Not Found":
                    logger.warning('Repository ' + self.owner + " " + self.repo + " may not exist")
                    return False
                else:
                    logger.error("Internal error: " + result)
                    logger.error('Repository' + self.owner + " " + self.repo)
                    logger.error("Token: " + self.pr_header['Authorization'])
                    raise WebsiteException
            return result
        except RequestException as e:
            if times < 5:
                logger.warning('Failure happen with ' + self.owner + " " + self.repo)
                times += 1
                return wrapper(self, times, *args, **kwargs)
            else:
                logger.error(
                    "Five time out at validate repo with " + self.owner + " " + self.repo)
                logger.error("Token: " + self.pr_header['Authorization'])
                logger.exception(e)
                raise TimeOutException
        except Exception as e:
            logger.error("Error at validation")
            raise Exception(e)

    return wrapper


def catch_deal_diff_error(func):
    def wrapper(self, item, times=0):
        logger = logging.getLogger('Diff ' + threading.current_thread().name[-3:])
        try:
            if times == 0:
                logger.debug("Start get diff:" + self.owner + " " + self.repo + " number:" + str(item["number"]))
            result = func(self, item)
            if not result:
                logger.error('Repository' + self.owner + " " + self.repo + " may not exist")
            return result
        except RequestException as e:
            if times < 5:
                logger.warning('Failure happen with ' + self.owner + " " + self.repo + " number:" + str(item["number"]))
                times += 1
                return wrapper(self, item, times)
            else:
                logger.error(
                    "Five time out at getting diff with " + self.owner + " " + self.repo + " number:" + str(item["number"]))
                logger.error("Token: " + self.pr_header['Authorization'])
                logger.exception(e)
                raise DiffException
        except Exception as e:
            logger.error("Error at getting diff")
            raise Exception(e)

    return wrapper


def catch_get_repo_info_error(func):
    def wrapper(self, times=0, *args, **kwargs):
        logger = logging.getLogger('Repo_info ' + threading.current_thread().name[-3:])
        try:
            result = func(self, *args, **kwargs)
            if 'message' in result:
                logger.warning("Internal error: " + self.owner + " " + self.repo)
                logger.warning(result['message'])
                logger.warning("Token: " + self.pr_header['Authorization'])
                raise RequestException
            return result
        except RequestException as e:
            if times < 5:
                logger.warning('Failure happen with' + self.owner + " " + self.repo)
                times += 1
                return wrapper(self, times, *args, **kwargs)
            else:
                logger.error(
                    "Five time out get repo info with " + self.owner + " " + self.repo)
                logger.exception(e)
                raise TimeOutException
        except Exception as e:
            logger.error("Internal error: " + self.owner + " " + self.repo)
            logger.exception(e)
            logger.error("Token: " + self.pr_header['Authorization'])
            raise WebsiteException

    return wrapper


def catch_get_max_pr_num_error(func):
    def wrapper(self, times=0, *args, **kwargs):
        logger = logging.getLogger('Max_pr ' + threading.current_thread().name[-3:])
        try:
            result = func(self, *args, **kwargs)
            if 'message' in result:
                logger.warning("Internal error: " + self.owner + " " + self.repo)
                logger.warning(result['message'])
                logger.warning("Token: " + self.pr_header['Authorization'])
                raise RequestException
            return result
        except RequestException as e:
            if times < 5:
                logger.warning('Failure happen with' + self.owner + " " + self.repo)
                times += 1
                return wrapper(self, times, *args, **kwargs)
            else:
                logger.error(
                    "Five time out at get repo max num with " + self.owner + " " + self.repo)
                logger.error("token:"+self.pr_header['Authorization'])
                logger.exception(e)
                raise TimeOutException
        except BaseException as e:
            logger.error("Internal error " + self.owner + " " + self.repo)
            logger.exception(e)
            logger.error("Token: " + self.pr_header['Authorization'])
            raise WebsiteException
        except Exception as e:
            logger.error("Error at get max num")
            logger.error("token:" + self.pr_header['Authorization'])
            logger.exception(e)
            raise Exception(e)

    return wrapper


def catch_get_pr_page_results_not_deal_error(func):
    def wrapper(self, tpage, times=0):
        logger = logging.getLogger('Page result ' + threading.current_thread().name[-3:])
        try:
            result =func(self, tpage)

            logger.debug('Getting ' + self.owner + " " + self.repo + " page: " + str(tpage))
            if 'message' in result:
                logger.warning("Internal error: " + self.owner + " " + self.repo)
                logger.warning(result['message'])
                logger.warning("Token: " + self.pr_header['Authorization'])
                raise RequestException

            return result

        except RequestException as e:
            if times < 5:
                logger.warning('Failure happen with ' + self.owner + " " + self.repo+" page: "+str(tpage))
                times += 1
                return wrapper(self,tpage,times)
            else:
                logger.error(
                            "Five time out at getting page with " + self.owner + " " + self.repo+" page: "+str(tpage))
                logger.exception(e)
                logger.debug("Repository: " + self.owner + " " + self.repo + " will exit")
                return []
        except Exception as e:
            logger.error("Error at get per page result")
            raise Exception(e)

    return wrapper
