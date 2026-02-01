# -*- coding: utf-8 -*-
import typing as ty

import logging

from .nlc import NLCProvider
from .base import BaseProvider
from .schemas import BookMetaSchema

LOG = logging.getLogger("book_mgr")

BOOK_META_PROVIDERS = (
    (NLCProvider.source, NLCProvider),
)


class BookMetaProvider(BaseProvider):

    def find_book_by_isbn(self, isbn: str) -> ty.Optional[BookMetaSchema]:
        for _, provider_cls in BOOK_META_PROVIDERS:
            provider = provider_cls()
            book_meta = provider.find_book_by_isbn(isbn)
            if book_meta:
                return book_meta

            LOG.info("Unable to retrieve book metadata for ISBN: %s "
                     "from provider: %s", (isbn, provider_cls.source))

        return None
