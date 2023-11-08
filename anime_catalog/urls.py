from django.urls import path
from . import views


urlpatterns = [
    path('short-anime/', views.ShortAnimeListAPIView.as_view()),
    path('full-anime/', views.FullAnimeListAPIView.as_view()),
    path('anime-create/', views.AnimeCreateAPIView.as_view()),
    path('anime-update/<int:pk>/', views.AnimeUpdateAPIView.as_view()),
    path('anime-delete/<int:pk>/', views.AnimeDeleteAPIView.as_view()),
    path('anime-retrieve/<int:pk>/', views.AnimeRetrieveAPIView.as_view()),
    path('anime-retrieve/<int:pk>/average-rating/', views.AnimeAverageRatingView.as_view()),
    path('anime-retrieve/<int:pk>/rating-count/', views.AnimeRatingDistributionView.as_view()),
    path('genre-list/', views.GenreListAPIView.as_view()),
    path('genre-retrieve/<int:pk>/', views.GenreRetrieveAPIView.as_view()),
    path('genre-create/', views.GenreCreateAPIView.as_view()),
    path('genre-update/<int:pk>/', views.GenreUpdateAPIView.as_view()),
    path('genre-delete/<int:pk>/', views.GenreDeleteAPIView.as_view()),
    path('studio-list/', views.StudioListAPIView.as_view()),
    path('studio-create/', views.StudioCreateAPIView.as_view()),
    path('studio-update/<int:pk>/', views.StudioUpdateAPIView.as_view()),
    path('studio-delete/<int:pk>/', views.StudioDeleteAPIView.as_view()),
    path('rating-create/', views.RatingCreateAPIView.as_view()),
    path('rating-update/<int:pk>/', views.RatingUpdateAPIView.as_view()),
    path('rating-delete/<int:pk>/', views.RatingDeleteAPIView.as_view()),
    path('collections/', views.CollectionListAPIView.as_view()),
    path('collection-create/', views.CollectionCreateAPIView.as_view()),
    path('collection-update/<int:pk>/', views.CollectionUpdateAPIView.as_view()),
    path('collection-delete/<int:pk>/', views.CollectionDeleteAPIView.as_view()),
    path('comments/', views.CommentsListAPIView.as_view()),
    path('data-from-drf/', views.data_from_drf, name='data_from_drf'),
    path('register/', views.UserRegistrationView.as_view(), name='user-registration'),
]

