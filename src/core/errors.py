from urllib.error import HTTPError


class NotFound(HTTPError):

    def __init__(self, parent=None, url=None, msg=None):
        if parent is not None:
            super().__init__(parent.url, parent.code, parent.msg, parent.hdrs,
                             parent.fp)
        else:
            super().__init__(url, '404', msg, None, None)
