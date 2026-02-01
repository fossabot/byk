# -*- coding : utf-8 -*-

from django.urls import path
from .routes import apis

urlpatterns = [
    path('api/', apis.urls),
]
