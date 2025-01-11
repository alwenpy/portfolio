from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("apply-changes/", views.apply_changes, name="apply_changes"),
    path("anime-of-the-day/", views.get_anime_of_the_day, name="get_anime_of_the_day"),
]