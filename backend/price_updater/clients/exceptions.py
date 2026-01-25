class MoexError(Exception):
    """Base error for Moex client"""


class MoexSessionNotOpened(MoexError):
    """Moex client session was not opened (aopen was not called)"""


class MoexHTTPError(MoexError):
    """Non 2xx response code from Moex API"""

    def __init__(self, status: int, body: str | None = None):
        self.status = status
        self.body = body
        super().__init__(f'MOEX HTTP {status}')


class MoexNetworkError(MoexError):
    """Network / timeout errors"""


class MoexParseError(MoexError):
    """Invalid JSON / unexpected schema"""
