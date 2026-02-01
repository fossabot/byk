# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import gettext as _

from .models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_authors', 'published_date', 'isbn_number')
    search_fields = ('title', 'authors', 'isbn_number')

    @staticmethod
    def display_authors(obj):
        return ", ".join(obj.authors) if obj.authors else _("Unknown")

    display_authors.short_description = _("Authors")


admin.site.register(Book, BookAdmin)
