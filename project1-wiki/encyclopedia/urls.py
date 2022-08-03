from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/add/", views.add, name="add"),
    path("wiki/random/", views.random, name="random"),
    path("wiki/<str:title>/", views.entry, name="entry-page"),
    path("wiki/<str:title>/edit/", views.edit, name="edit"),
]
