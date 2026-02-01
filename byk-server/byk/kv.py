# -*- coding: utf-8 -*-
import typing as ty  # noqa: F401

from redis.asyncio import from_url
from django.utils.functional import LazyObject
from django.conf import Settings, settings


def create_redis_client():
    r = from_url(settings.REDIS_URL)
    return r


class LazyRedis(LazyObject):
    def _setup(self):
        self._wrapped = create_redis_client()
        self._wrapped.ping()  # Force connection on setup


redis = LazyRedis()
