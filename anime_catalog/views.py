from django.db.models import Avg, Count
from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, \
    RetrieveAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Anime, Genre, Studio, Rating
from . import serializers
from rest_framework import permissions, status
from .permissons import IsModerator
import requests

from .serializers import AnimeAverageRatingSerializer, UserRegistrationSerializer


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


class AnimeAverageRatingView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        anime = get_object_or_404(Anime, pk=pk)
        average_rating = Rating.objects.filter(for_anime=anime).aggregate(Avg('rate'))['rate__avg']

        if average_rating is not None:
            serializer = AnimeAverageRatingSerializer({'average_rating': average_rating})
            return Response(serializer.data)
        else:
            return Response({'detail': 'No rating.'}, status=404)


class AnimeRatingDistributionView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        anime = get_object_or_404(Anime, pk=pk)
        rating_distribution = Rating.objects.filter(for_anime=anime).values('rate').annotate(count=Count('rate')).order_by('rate')

        rating_data = {}
        for item in rating_distribution:
            rating = item['rate']
            count = item['count']
            rating_data[rating] = count

        return Response(rating_data)


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def data_from_drf(request):
    response = requests.get('http://127.0.0.1:8000/catalog_api/full-anime/')

    if response.status_code == 200:
        data = response.json()
        context = {'data': data}
        return render(request, 'home.html', context)
