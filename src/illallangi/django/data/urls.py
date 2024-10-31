import djp
from django.contrib import admin
from django.urls import re_path

from illallangi.django.data import views

urlpatterns = [
    re_path(
        r"^admin/",
        admin.site.urls,
    ),
    *djp.urlpatterns(),
    re_path(
        r"^favicon.svg",
        views.favicon,
        name="favicon",
    ),
    re_path(
        r"^favicon.ico",
        views.favicon,
    ),
    re_path(
        r"^$",
        views.home_list,
        name="home_list",
    ),
]
