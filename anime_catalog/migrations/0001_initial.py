# Generated by Django 4.2.6 on 2023-11-01 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Studio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Anime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default='static/pics/empty.svg', upload_to='anime_images/')),
                ('title', models.CharField(max_length=516)),
                ('description', models.TextField()),
                ('type', models.CharField(max_length=64)),
                ('episodes', models.PositiveSmallIntegerField()),
                ('ready_episodes', models.PositiveSmallIntegerField()),
                ('length_of_episodes', models.PositiveSmallIntegerField()),
                ('status', models.CharField(max_length=64)),
                ('age_rating', models.CharField(max_length=36)),
                ('genres', models.ManyToManyField(to='anime_catalog.genre')),
                ('studio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anime_catalog.studio')),
            ],
        ),
    ]
