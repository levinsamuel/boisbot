from urllib.error import HTTPError


class NotFound(HTTPError):

    def __init__(self, parent):
        super().__init__(parent.url, parent.code, parent.msg, parent.hdrs,
                         parent.fp)

    def __init__(self, url, msg):
        super().__init__(url, '404', msg, None, None)
