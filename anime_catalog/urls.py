from django.urls import path
from . import views


urlpatterns = [
    path('short-anime/', views.ShortAnimeListAPIView.as_view()),
    path('full-anime/', views.FullAnimeListAPIView.as_view()),
    path('anime-create/', views.AnimeCreateAPIView.as_view()),
    path('anime-update/<int:pk>/', views.AnimeUpdateAPIView.as_view()),
    path('anime-delete/<int:pk>/', views.AnimeDeleteAPIView.as_view()),
    path('anime-retrieve/<int:pk>/', views.AnimeRetrieveAPIView.as_view()),
    path('genre-list/', views.GenreListAPIView.as_view()),
    path('genre-retrieve/<int:pk>/', views.GenreRetrieveAPIView.as_view()),
    path('genre-create/', views.GenreCreateAPIView.as_view()),
    path('genre-update/<int:pk>/', views.GenreUpdateAPIView.as_view()),
    path('genre-delete/<int:pk>/', views.GenreDeleteAPIView.as_view()),
    path('studio-list/', views.StudioListAPIView.as_view()),
    path('studio-create/', views.StudioCreateAPIView.as_view()),
    path('studio-update/<int:pk>/', views.StudioUpdateAPIView.as_view()),
    path('studio-delete/<int:pk>/', views.StudioDeleteAPIView.as_view()),
    path('data-from-drf/', views.data_from_drf, name='data_from_drf'),
]

