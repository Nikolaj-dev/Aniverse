from django.contrib import admin
from .models import Anime, Genre, Studio, Profile, Rating, Collection, Comment, Review


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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'anime', 'created_at')
    list_filter = ('anime',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'anime', 'final_grade', 'date')
    list_filter = ('anime', 'user__user__username', 'final_grade')
    search_fields = ('anime__title', 'user__user__username', 'text')

    def user(self, obj):
        return obj.user.user.username

    user.admin_order_field = 'user__user__username'
