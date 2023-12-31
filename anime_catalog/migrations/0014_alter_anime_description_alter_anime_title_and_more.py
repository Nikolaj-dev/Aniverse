# Generated by Django 4.2.6 on 2023-11-09 12:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime_catalog', '0013_alter_review_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anime',
            name='description',
            field=models.TextField(validators=[django.core.validators.MinLengthValidator(100), django.core.validators.MaxLengthValidator(5000)]),
        ),
        migrations.AlterField(
            model_name='anime',
            name='title',
            field=models.CharField(max_length=516, unique=True),
        ),
        migrations.AlterField(
            model_name='anime',
            name='year',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2023)]),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(validators=[django.core.validators.MaxLengthValidator(250)]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(250)]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='profile_images/empty.jpg', upload_to='profile_images/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='nickname',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(validators=[django.core.validators.MinLengthValidator(150), django.core.validators.MaxLengthValidator(10000)]),
        ),
    ]
