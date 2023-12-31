# Generated by Django 4.2.6 on 2023-11-07 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('anime_catalog', '0009_alter_genre_title_alter_studio_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('anime', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anime_catalog.anime')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='anime_catalog.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anime_catalog.profile')),
            ],
        ),
    ]
