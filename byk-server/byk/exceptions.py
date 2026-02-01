# -*- coding: utf-8 -*-


class BykException(Exception):
    """Base Byk exception."""
    pass


class NotAuthenticated(BykException):
    """Raised when authentication fails."""
    pass
