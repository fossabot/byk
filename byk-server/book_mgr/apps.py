from django.apps import AppConfig


class BookMgrConfig(AppConfig):
    name = 'book_mgr'

    def ready(self):
        from . import signal_handlers  # noqa: F401
