# -*- coding: utf-8 -*-
import typing as ty  # noqa: F401

from django.utils.functional import LazyObject
from faststream.redis.broker import RedisBroker


# class LazyBroker(LazyObject):
#
#     def _setup(self) -> None:
#         from django.conf import settings
#         self._wrapped = RedisBroker(settings.REDIS_URL)

def create_broker() -> RedisBroker:
    from django.conf import settings
    return RedisBroker(settings.REDIS_URL)

broker = create_broker()
