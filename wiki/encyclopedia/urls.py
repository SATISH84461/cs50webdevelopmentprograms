from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/new_page",views.new_page, name="new_page"),
    path("wiki/search_result",views.search_result, name="search_result"),
    path("wiki/random_page",views.random_page, name="random_page"),
    path("wiki/<str:name>",views.gget_page, name="gget_page"),
    path("wiki/<str:name>/edit_page",views.edit_page, name="edit_page"),
]
