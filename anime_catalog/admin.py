from django.contrib import admin
from .models import Anime, Genre, Studio, Profile, Rating, Collection


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


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'sex', 'birth_date')
    list_filter = ('sex', 'birth_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('for_user', 'for_anime', 'rate')
    list_filter = ('rate',)
    search_fields = (
        'for_user__user__username',
        'for_user__user__first_name',
        'for_user__user__last_name', 'for_anime__title'
    )


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_filter = ('user',)
    search_fields = ('name', 'user__user__username', 'user__user__first_name', 'user__user__last_name')