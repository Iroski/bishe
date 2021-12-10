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
    def wrapper(self,page=0, times=0):
        logger = logging.getLogger('Max_pr ' + threading.current_thread().name[-3:])
        try:
            result = func(self,page)
            if type(result) is int:
                return result
            if 'message' in result:
                logger.warning("Internal error: " + self.owner + " " + self.repo)
                logger.warning(result['message'])
                logger.warning("Token: " + self.pr_header['Authorization'])
                raise RequestException
        except RequestException as e:
            if times < 5:
                logger.warning('Failure happen with' + self.owner + " " + self.repo)
                times += 1
                return wrapper(self,page, times)
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

def catch_get_issue_error(func):
    def wrapper(self,number, times=0):
        logger = logging.getLogger('issue ' + threading.current_thread().name[-3:])
        try:
            result = func(self,number)
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
                return wrapper(self,number, times)
            else:
                logger.error(
                    "Five time out at get issue with " + self.owner + " " + self.repo)
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

def catch_get_popular_repo_per_page_error(func):
    def wrapper(self, language, page, per_page, times=0):
        logger = logging.getLogger('Popular page ' + threading.current_thread().name[-3:])
        try:
            result =func(self, language, page, per_page)

            logger.debug('Getting popular: ' + language + " page: " + str(page))
            if 'message' in result:
                logger.warning("Internal error: " + 'Getting popular: ' + language + " page: " + str(page))
                logger.warning(result['message'])
                logger.warning("Token: " + self.pr_header['Authorization'])
                raise RequestException

            return result

        except RequestException as e:
            if times < 5:
                logger.warning('Failure happen with ' + 'Getting popular: ' + language+" page: "+str(page))
                times += 1
                return wrapper(self, language, page, per_page,times)
            else:
                logger.error(
                            "Five time out at getting popular: " + language+" page: "+str(page))
                logger.exception(e)
                raise TimeOutException
        except Exception as e:
            logger.error("Error at get popular page result")
            raise Exception(e)

    return wrapper