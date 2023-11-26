from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
from datetime import datetime


current_year = datetime.now().year


class Anime(models.Model):
    image = models.ImageField(upload_to='anime_images/', default='anime_images/empty.png', blank=True, null=False)
    title = models.CharField(max_length=516, unique=True)
    description = models.TextField(validators=[MinLengthValidator(100), MaxLengthValidator(5000)])
    type = models.CharField(max_length=64)
    episodes = models.PositiveSmallIntegerField()
    ready_episodes = models.PositiveSmallIntegerField()
    length_of_episodes = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=64)
    genres = models.ManyToManyField('Genre')
    age_rating = models.CharField(max_length=36)
    studio = models.ForeignKey('Studio', on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(current_year)])

    def __str__(self):
        return self.title


class Genre(models.Model):
    title = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.title


class Studio(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title


class Profile(models.Model):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

    SEX_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    )

    nickname = models.CharField(max_length=64, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', default='profile_images/empty.jpg', blank=True, null=False)
    bio = models.TextField(validators=[MaxLengthValidator(250)], blank=True, null=True)
    sex = models.CharField(choices=SEX_CHOICES)
    birth_date = models.DateField()

    def __str__(self):
        return self.nickname

    def save(self, *args, **kwargs):
        if not self.image:
            self.image = 'profile_images/empty.jpg'

        super(Profile, self).save(*args, **kwargs)


class Rating(models.Model):
    for_anime = models.OneToOneField('Anime', on_delete=models.CASCADE)
    for_user = models.OneToOneField('Profile', on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return f"{self.for_user.user.first_name} rates {self.for_anime} as {self.rate}"


class Collection(models.Model):
    name = models.CharField(max_length=128)
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    items = models.ManyToManyField('Anime')

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    anime = models.ForeignKey('Anime', on_delete=models.CASCADE)
    text = models.TextField(validators=[MaxLengthValidator(250)])
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"{self.user.user.username} - {self.anime.title} - {self.created_at}"


class Review(models.Model):
    anime = models.ForeignKey('Anime', on_delete=models.CASCADE)
    storyline = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    characters = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    artwork = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    sound_series = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    final_grade = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField(validators=[MinLengthValidator(150), MaxLengthValidator(10000)])
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'anime')

    def __str__(self):
        return f"{self.user.user.username} - {self.anime.title} - {self.final_grade}"
