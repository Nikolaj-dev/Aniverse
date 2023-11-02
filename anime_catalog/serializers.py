from rest_framework import serializers
from .models import Anime, Genre, Studio


class ShortAnimeSerializer(serializers.ModelSerializer):
    studio = serializers.SlugRelatedField(many=False, queryset=Studio.objects.all(), slug_field='title')

    class Meta:
        model = Anime
        fields = ('title', 'image', 'studio', 'year')


class FullAnimeSerializer(serializers.ModelSerializer):
    studio = serializers.SlugRelatedField(many=False, queryset=Studio.objects.all(), slug_field='title')
    genres = serializers.SlugRelatedField(many=True, queryset=Genre.objects.all(), slug_field='title')

    class Meta:
        model = Anime
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = '__all__'

