# -*- coding: utf-8 -*-
import typing as ty  # noqa: F401

import asyncio
from asgiref.sync import async_to_sync
from django.apps import AppConfig


class RootConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "byk"

    def ready(self) -> None:
        from byk.task_broker.base import broker

        async_to_sync(broker.connect)()
