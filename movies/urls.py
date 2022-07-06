from django.urls import path
from movies.views import ActorView, MovieView, ActorAndMovieView

urlpatterns = [
    path('/actors', ActorView.as_view()),
    path('/movies', MovieView.as_view()),
    path('/actors_and_movies', ActorAndMovieView.as_view())
]