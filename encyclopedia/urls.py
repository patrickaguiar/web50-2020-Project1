from django.urls import path

from . import views

app_name='encyclopedia'

urlpatterns = [
    path("", views.index, name='index'),
    path("wiki/", views.wiki, name="wiki"),
    path("<str:entry_name>", views.entry, name='entry'),
    path("search/", views.search, name='search'),
    path("create_new_page/", views.create_new_page, name='create_new_page'),
    path("edit_entry/", views.edit_entry, name='edit_entry'),
    path("random_entry/", views.random_entry, name='random_entry'),
]
