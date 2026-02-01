# -*- coding: utf-8 -*-
import typing as ty  # noqa: F401

import logging
import time

from django.db import transaction
from byk.task_broker import broker
from book_mgr.models import Book

LOG = logging.getLogger("book_mgr")

@broker.subscriber("book_mgr.fetch_books")
def fetch_books_task(pk: ty.AnyStr) -> None:
    from book_mgr.providers.book_meta import BookMetaProvider

    time.sleep(1)  # Sleep to ensure DB transaction is committed

    ins = Book.objects.get(id=pk)

    provider = BookMetaProvider()
    book_meta = provider.find_book_by_isbn(ins.isbn_number)
    if not book_meta:
        return

    with transaction.atomic():
        ins.title = book_meta.title
        ins.authors = book_meta.authors or list()
        ins.tags = book_meta.tags or list()
        ins.published_date = book_meta.published_date or ins.published_date
        ins.comments = book_meta.description or ins.comments
        ins.save()

    LOG.info("Fetched and updated book metadata for Book ID: %s", pk)
