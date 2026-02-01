# -*- coding: utf-8 -*-
import typing as ty  # noqa: F401

from ninja import Schema

ERROR_OBJECT_NOT_FOUND = "object_not_found"
ERROR_OBJECT_EXISTS = "object_exists"
SUCCEED = "succeed"
NOT_AUTHENTICATED = "not_authenticated"
AUTHENTICATION_FAILURE = "authentication_failure"


class ErrorMessageSchema(Schema):
    error_code: str = None
    message: str = None
