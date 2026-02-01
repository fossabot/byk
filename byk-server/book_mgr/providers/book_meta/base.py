# -*- coding: utf-8 -*-
import typing as ty  # noqa: F401

from .schemas import BookMetaSchema


class BaseProvider(object):

    def fetch_metadata(self, identifier: str) -> ty.Dict[str, ty.Any]:
        raise NotImplementedError()

    def find_book_by_isbn(self, isbn: str) -> ty.Optional[BookMetaSchema]:
        meta_ = self.fetch_metadata(isbn)
        if not meta_:
            return None

        return BookMetaSchema(**meta_)
