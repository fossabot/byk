# -*- coding: utf-8 -*-
import typing as ty  # noqa: F401

from pydantic import Field
from ninja import ModelSchema
from .models import Book, BookStorage, Tag


class TagSchema(ModelSchema):
    class Meta:
        model = Tag
        exclude = ["comments"]


class BookStorageSchema(ModelSchema):

    class Meta:
        model = BookStorage
        exclude = ["comments"]


class BookSchema(ModelSchema):
    categories: ty.List[TagSchema] = Field(default_factory=list)
    location: BookStorageSchema = None

    @staticmethod
    def resolve_categories(book: Book) -> ty.List[Tag]:
        return list(book.tags.all())

    class Meta:
        model = Book
        fields = "__all__"


class BookCreateSchema(ModelSchema):

    class Meta:
        model = Book
        exclude = ["id", "location"]
