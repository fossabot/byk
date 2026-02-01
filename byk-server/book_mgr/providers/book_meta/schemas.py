# -*- coding: utf-8 -*-
import typing as ty  # noqa: F401

from pydantic import BaseModel, Field, AliasChoices


class BookMetaSchema(BaseModel):
    title: str = Field(..., description="Title of the book")
    authors: ty.List[str] = Field(default_factory=list, description="List of authors of the book")
    publisher: ty.Optional[str] = Field(None, description="Publisher of the book")
    published_date: ty.Optional[str] = Field(None,
                                             validation_alias=AliasChoices('published_date', 'pubdate'),
                                             description="Published date of the book")
    description: ty.Optional[str] = Field(None, description="Description or summary of the book")
    isbn: ty.Optional[str] = Field(None, description="ISBN identifier")
    tags: ty.List[str] = Field(default_factory=list,
                               validation_alias=AliasChoices('categories', 'tags'),
                               description="Categories or genres of the book")
