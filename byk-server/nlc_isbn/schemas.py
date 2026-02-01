# -*- coding: utf-8 -*-
# Copyright (C) 2025-present <andrija.junzki AT gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import typing as ty  # noqa: F401

from pydantic import BaseModel, Field


class BookMetadataSchema(BaseModel):
    title: str = None
    authors: ty.List[str] = Field(default_factory=list)
    publisher: str = None
    published_at: str = Field(alias='pubdate')
    comments: str = None
    isbn: str = None
    tags: ty.List[str] = Field(default_factory=list)
