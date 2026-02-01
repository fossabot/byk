# -*- coding: utf-8 -*-
import typing as ty  # noqa: F401

from django.dispatch import receiver
from django.db.models.signals import post_save
from book_mgr.models import Book


@receiver(post_save, sender=Book)
async def on_book_saved(sender: ty.Type[Book], instance: Book, created: bool, **kwargs: ty.Any):
    from byk.task_broker import broker

    if not created:
        return

    await broker.publish(str(instance.id), "book_mgr.fetch_books")
