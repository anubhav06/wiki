from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("newpage/", views.newPage, name="newPage"),
    path("wiki/<str:title>/editPage", views.editPage, name="editPage"),
    path("randomPage/", views.randomPage, name="randomPage")
]
