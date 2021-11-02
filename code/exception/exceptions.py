class BaseException(Exception):
    def __init__(self, *args, **kwargs):
        super(BaseException, self).__init__(*args, **kwargs)


class WebsiteException(BaseException): ...


class DiffException(BaseException): ...


class TimeOutException(BaseException): ...
