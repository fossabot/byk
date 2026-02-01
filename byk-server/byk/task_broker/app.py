# -*- coding: utf-8 -*-
import typing as ty  # noqa: F401

import os
import sys
import importlib

import django
from django.utils.functional import LazyObject
from faststream import FastStream
from .base import broker


def create_faststream_app() -> FastStream:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'byk.settings')
    print(f"!!! ENV DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}", file=sys.stderr)

    django.setup()  # Setup Django to load models, settings and tasks

    from django.conf import settings



    app_ = FastStream(broker)
    return app_


class LazyApp(LazyObject):

    def _setup(self) -> None:
        self._wrapped = create_faststream_app()


faststream_app = create_faststream_app()

@faststream_app.on_startup
async def on_startup() -> None:
    from django.conf import settings
    print(f"!!! FastStream App started with Redis URL: {settings.REDIS_URL}", file=sys.stderr)

    for task_module in settings.FASTSTREAM_TASK_MODULES:
        importlib.import_module(task_module)
