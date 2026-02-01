"""
URL configuration for byk-server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from ninja import NinjaAPI
from byk.authentication import token_auth, on_invalid_token
from byk.exceptions import NotAuthenticated

apis = NinjaAPI(auth=token_auth)
apis.exception_handler(NotAuthenticated)(on_invalid_token(apis))

apis.add_router('books/', 'book_mgr.routes.apis')
apis.add_router('accounts/', 'accounts.routes.apis')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', apis.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
