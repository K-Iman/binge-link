from django.urls import path
from core import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("library/", views.library, name="library"),
    path("movie/<int:movie_id>/", views.movie_detail, name="movie_detail"),
    path("tv/<int:tv_id>/", views.tv_detail, name="tv_detail"),
    path("popular/", views.popular, name="popular"),
    path("genre/<int:genre_id>/", views.browse_genre, name="browse_genre"),
]
