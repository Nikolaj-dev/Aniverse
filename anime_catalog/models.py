from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Anime(models.Model):
    image = models.ImageField(upload_to='anime_images/', default='anime_images/empty.png', blank=True, null=False)
    title = models.CharField(max_length=516)
    description = models.TextField()
    type = models.CharField(max_length=64)
    episodes = models.PositiveSmallIntegerField()
    ready_episodes = models.PositiveSmallIntegerField()
    length_of_episodes = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=64)
    genres = models.ManyToManyField('Genre')
    age_rating = models.CharField(max_length=36)
    studio = models.ForeignKey('Studio', on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.title


class Genre(models.Model):
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title


class Studio(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', default='profile_images/empty.jpg')
    bio = models.TextField()
    sex = models.CharField(choices=(('male', 'Male'), ('female', 'Female'), ('other', 'Other')))
    birth_date = models.DateField()

    def __str__(self):
        return self.user.first_name


class Rating(models.Model):
    for_anime = models.ForeignKey('Anime', on_delete=models.CASCADE)
    for_user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return f"{self.for_user.user.first_name} rates {self.for_anime} as {self.rate}"


class Collection(models.Model):
    name = models.CharField(max_length=128)
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    items = models.ManyToManyField('Anime')

    def __str__(self):
        return self.name
