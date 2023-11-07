from rest_framework import serializers
from .models import Anime, Genre, Studio, Profile, Rating, Collection
from django.contrib.auth.models import User


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


class AnimeAverageRatingSerializer(serializers.Serializer):
    average_rating = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    image = serializers.ImageField(required=False)
    bio = serializers.CharField(required=False)
    sex = serializers.ChoiceField(choices=Profile.SEX_CHOICES, required=False)
    birth_date = serializers.DateField(required=False)

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'image', 'bio', 'sex', 'birth_date')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        profile_data = {
            'user': user,
            'image': validated_data.get('image'),
            'bio': validated_data.get('bio'),
            'sex': validated_data.get('sex'),
            'birth_date': validated_data.get('birth_date'),
        }
        Profile.objects.create(**profile_data)
        return user


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RatingSerializer, self).__init__(*args, **kwargs)
        self.fields['for_user'].required = False


class CollectionSerializer(serializers.ModelSerializer):
    items = serializers.SlugRelatedField(
        many=True,
        slug_field='title',
        queryset=Anime.objects.all()
    )

    class Meta:
        model = Collection
        fields = ('name', 'items')

    def create(self, validated_data):
        user = Profile.objects.get(user=self.context['request'].user)
        items_data = validated_data.pop('items', [])
        collection = Collection.objects.create(user=user, **validated_data)

        for item_title in items_data:
            item = Anime.objects.get(title=item_title)
            collection.items.add(item)

        return collection