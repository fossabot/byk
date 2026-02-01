# -*- coding: utf-8 -*-
import typing as ty  # noqa: F401

import uuid
from byk.contexts.requests import request_id_var, client_ip_var


class RequestTracingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. 优先获取 Next.js 传来的 Request ID，否则生成新的
        req_id = request.headers.get("X-Request-ID", 'req-%s' % str(uuid.uuid7()))

        # 2. 获取真实的 Client IP (考虑代理情况)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        # 3. 绑定到当前线程上下文
        request_id_var.set(req_id)
        client_ip_var.set(ip)

        response = self.get_response(request)

        # 4. 将 ID 返给 Client 方便调试
        response["X-Request-ID"] = req_id
        return response
