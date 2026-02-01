# -*- coding: utf-8 -*-
import typing as ty  # noqa: F401

import uuid
import contextvars

request_id_var = contextvars.ContextVar("request_id", default="")
client_ip_var = contextvars.ContextVar("client_ip", default="")

def get_request_id():
    return request_id_var.get()

def get_client_ip():
    return client_ip_var.get()
