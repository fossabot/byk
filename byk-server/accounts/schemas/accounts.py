# -*- coding: utf-8 -*-
import typing as ty  # noqa: F401

from pydantic import Field
from ninja import Schema


class UserLoginRequestSchema(Schema):
    username: str
    password: str
    tenant: str = Field(default='default')  # Default tenant


class TokenCreatedResponseSchema(Schema):
    access_token: str
    token_type: str = "bearer"
