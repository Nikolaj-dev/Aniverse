from django.db import models


class Anime(models.Model):
    image = models.ImageField(upload_to='anime_images/', default='static/pics/empty.svg', blank=True, null=False)
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

