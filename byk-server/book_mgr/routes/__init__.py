# -*- coding: utf-8 -*-

from byk.schemas import NOT_AUTHENTICATED
from ninja.errors import AuthenticationError

from .books import *  # noqa: F401
from .router import router as apis


# @apis.exception_handler(AuthenticationError)
# def on_invalid_token(request, exc):
#     return apis.create_response(request, {
#         "message": str(exc),
#         "error_code": NOT_AUTHENTICATED
#     }, status=401)
