# -*- coding: utf-8 -*-
import typing as ty  # noqa: F401

import logging

from nlc_isbn import isbn2meta
from .base import BaseProvider

LOG = logging.getLogger("book_mgr")


class NLCProvider(BaseProvider):
    source = 'NLC'  # Chinese National Library

    def fetch_metadata(self, identifier: str) -> ty.Dict[str, ty.Any]:
        return isbn2meta(identifier, LOG)
