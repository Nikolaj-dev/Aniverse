from django.contrib import admin
from .models import Anime, Genre, Studio


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'episodes', 'ready_episodes', 'length_of_episodes', 'status', 'age_rating')
    list_filter = ('type', 'status', 'age_rating')
    search_fields = ('title', 'description')
    filter_horizontal = ('genres',)
