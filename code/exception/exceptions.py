class BaseException(Exception):
    def __init__(self, *args, **kwargs):
        super(BaseException, self).__init__(*args, **kwargs)


''' this exception may happen when token is expired
    but network is ok'''
class WebsiteException(BaseException): ...


'''this exception happen when getting diff files wrong'''
class DiffException(BaseException): ...


''' this exception happen when netnet work has something wrong
    system will exit as for that period, network will always fail'''
class TimeOutException(BaseException): ...
