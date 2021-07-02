"""ideathon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', main, name="main"),
    path('search/map/<str:keyword>/', map, name='map'),
    path('search/map/<str:keyword>/<str:addr>/<str:place_name>/', getData, name='getData'),
    path('search/', search, name="search"),
    path('info_list/', info_list, name="info_list"),
    path('makedb/', makedb, name="makedb"),
    path('info_list/<int:id>/', info_list_detail, name="info_list_detail")
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
