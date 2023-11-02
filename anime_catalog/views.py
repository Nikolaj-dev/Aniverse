from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, RetrieveAPIView
from .models import Anime, Genre, Studio
from . import serializers
from rest_framework import permissions
from .permissons import IsModerator
import requests


class ShortAnimeListAPIView(ListAPIView):
    queryset = Anime.objects.all()
    serializer_class = serializers.ShortAnimeSerializer
    permission_classes = [permissions.AllowAny]


class FullAnimeListAPIView(ListAPIView):
    serializer_class = serializers.FullAnimeSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Anime.objects.all()
        studio = self.request.query_params.get('studio')
        genres = self.request.query_params.getlist('genres')
        status = self.request.query_params.get('status')
        age_rating = self.request.query_params.get('age_rating')
        year = self.request.query_params.get('year')
        type = self.request.query_params.get('type')

        if studio:
            queryset = queryset.filter(studio__title=studio)
        if genres:
            queryset = queryset.filter(genres__title__in=genres)
        if status:
            queryset = queryset.filter(status=status)
        if age_rating:
            queryset = queryset.filter(age_rating=age_rating)
        if year:
            queryset = queryset.filter(year=year)
        if type:
            queryset = queryset.filter(type=type)

        return queryset


class AnimeRetrieveAPIView(RetrieveAPIView):
    queryset = Anime.objects.all()
    serializer_class = serializers.FullAnimeSerializer
    permission_classes = [permissions.AllowAny]


class AnimeCreateAPIView(CreateAPIView):
    queryset = Anime.objects.all()
    serializer_class = serializers.FullAnimeSerializer
    permission_classes = [permissions.IsAuthenticated, (permissions.IsAdminUser | IsModerator)]


class AnimeUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Anime.objects.all()
    serializer_class = serializers.FullAnimeSerializer
    permission_classes = [permissions.IsAuthenticated, (permissions.IsAdminUser | IsModerator)]


class AnimeDeleteAPIView(RetrieveDestroyAPIView):
    queryset = Anime.objects.all()
    serializer_class = serializers.FullAnimeSerializer
    permission_classes = [permissions.IsAuthenticated, (permissions.IsAdminUser | IsModerator)]


class GenreListAPIView(ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = [permissions.AllowAny]


class GenreRetrieveAPIView(RetrieveAPIView):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = [permissions.AllowAny]


class GenreCreateAPIView(CreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = [permissions.IsAuthenticated, (permissions.IsAdminUser | IsModerator)]


class GenreUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = [permissions.IsAuthenticated, (permissions.IsAdminUser | IsModerator)]


class GenreDeleteAPIView(RetrieveDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = [permissions.IsAuthenticated, (permissions.IsAdminUser | IsModerator)]


class StudioListAPIView(ListAPIView):
    queryset = Studio.objects.all()
    serializer_class = serializers.StudioSerializer
    permission_classes = [permissions.AllowAny]


class StudioCreateAPIView(CreateAPIView):
    queryset = Studio.objects.all()
    serializer_class = serializers.StudioSerializer
    permission_classes = [permissions.IsAuthenticated, (permissions.IsAdminUser | IsModerator)]


class StudioUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Studio.objects.all()
    serializer_class = serializers.StudioSerializer
    permission_classes = [permissions.IsAuthenticated, (permissions.IsAdminUser | IsModerator)]


class StudioDeleteAPIView(RetrieveDestroyAPIView):
    queryset = Studio.objects.all()
    serializer_class = serializers.StudioSerializer
    permission_classes = [permissions.IsAuthenticated, (permissions.IsAdminUser | IsModerator)]


def data_from_drf(request):
    response = requests.get('http://127.0.0.1:8000/catalog_api/full-anime/')

    if response.status_code == 200:
        data = response.json()
        context = {'data': data}
        return render(request, 'home.html', context)
