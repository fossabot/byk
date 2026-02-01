# -*- coding: utf-8 -*-
import typing as ty  # noqa: F401

import logging
from byk.contexts.requests import get_client_ip, get_request_id


class RequestTracingFilter(logging.Filter):
    def filter(self, record):
        # 将 context 里的值注入到 record 对象中
        record.request_id = get_request_id()
        record.client_ip = get_client_ip()
        return True
