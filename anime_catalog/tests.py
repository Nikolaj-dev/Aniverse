from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from .models import Anime, Genre, Studio, Profile, Rating, Collection, Comment, Review
from django.contrib.auth.models import User, Group


class ShortAnimeListAPITest(APITestCase):
    def setUp(self):
        # Create some sample data for testing
        studio = Studio.objects.create(title='Studio 1')
        Anime.objects.create(
            title='Anime 1',
            description='Test description',
            type='TV',
            episodes=12,
            ready_episodes=12,
            length_of_episodes=24,
            status='Ongoing',
            age_rating='PG-13',
            studio=studio,
            year=2022,
        )

    def test_get_short_anime_list(self):
        url = '/catalog_api/short-anime/'

        # Make a GET request to the endpoint
        response = self.client.get(url)

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0]['title'], 'Anime 1')
        self.assertEqual(response.data[0]['studio'], 'Studio 1')


class FullAnimeListAPITest(APITestCase):
    def setUp(self):
        # Create some sample data for testing
        studio = Studio.objects.create(title='Studio 1')
        genre1 = Genre.objects.create(title='Genre 1')
        genre2 = Genre.objects.create(title='Genre 2')

        anime1 = Anime.objects.create(
            title='Anime 1',
            studio=studio,
            age_rating='PG-13',
            year=2022,
            type='TV',
            status='Ongoing',
            episodes=12,
            ready_episodes=12,
            length_of_episodes=13,
        )
        anime1.genres.set([genre1, genre2])

        anime2 = Anime.objects.create(
            title='Anime 2',
            studio=studio,
            age_rating='R',
            year=2023,
            type='Movie',
            status='Completed',
            episodes=12,
            ready_episodes=12,
            length_of_episodes=13,
        )
        anime2.genres.set([genre1])

    def test_full_anime_list_with_filters(self):
        url = '/catalog_api/full-anime/'

        # Set up query parameters for the test
        params = {
            'studio': 'Studio 1',
            'genres': ['Genre 1', 'Genre 2'],
            'status': 'Ongoing',
            'age_rating': 'PG-13',
            'year': '2022',
            'type': 'TV',
            'episodes': 12,
            'ready_episodes': 12,
            'length_of_episodes': 13,
        }

        # Make a GET request to the endpoint with query parameters
        response = self.client.get(url, params)

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Anime 1')

    def test_full_anime_list_without_filters(self):
        url = '/catalog_api/full-anime/'

        # Make a GET request to the endpoint without query parameters
        response = self.client.get(url)

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AnimeRetrieveAPITest(APITestCase):
    def setUp(self):
        # Create some sample data for testing
        studio = Studio.objects.create(title='Studio 1')
        genre1 = Genre.objects.create(title='Genre 1')
        genre2 = Genre.objects.create(title='Genre 2')

        self.anime = Anime.objects.create(
            title='Anime 1',
            description='Test description',
            type='TV',
            episodes=12,
            ready_episodes=12,
            length_of_episodes=24,
            status='Ongoing',
            age_rating='PG-13',
            studio=studio,
            year=2022,
        )
        self.anime.genres.set([genre1, genre2])

    def test_retrieve_anime(self):
        url = f'/catalog_api/anime-retrieve/{self.anime.id}/'  # Update the URL if necessary

        # Make a GET request to the endpoint
        response = self.client.get(url)

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['title'], 'Anime 1')
        self.assertEqual(response.data['studio'], 'Studio 1')


class AnimeCreateAPITest(APITestCase):
    def setUp(self):
        # Create a test user with necessary permissions
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Get or create the 'Moderators' group
        moderators_group, created = Group.objects.get_or_create(name='Moderators')

        # Assign the user to the 'Moderators' group
        self.user.groups.add(moderators_group)

        # Create necessary Studio and Genre objects
        Studio.objects.create(title='Studio 1')
        Genre.objects.create(title='Genre 1')
        Genre.objects.create(title='Genre 2')

        # Use the created objects in anime_data
        self.anime_data = {
            'title': 'Test Anime',
            'description': 'This is a test anime description. This is a test anime description.This is a test anime description.This is a test anime description.This is a test anime description.This is a test anime description.This is a test anime description.This is a test anime description.This is a test anime description.This is a test anime description.This is a test anime description.This is a test anime description.This is a test anime description.This is a test anime description.',
            'type': 'TV',
            'episodes': 12,
            'ready_episodes': 12,
            'length_of_episodes': 24,
            'status': 'Ongoing',
            'genres': ['Genre 1', 'Genre 2'],
            'age_rating': 'PG-13',
            'studio': 'Studio 1',
            'year': 2023,
        }

        # Generate a JWT token for the user
        self.token = str(AccessToken.for_user(self.user))

    def test_create_anime(self):
        url = '/catalog_api/anime-create/'

        # Set the Authorization header with the JWT token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Make a POST request to create the Anime instance
        response = self.client.post(url, self.anime_data, format='json')

        # Check if the response status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AnimeUpdateAPITest(APITestCase):
    def setUp(self):
        # Create a test user with necessary permissions
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Get or create the 'Moderators' group
        moderators_group, created = Group.objects.get_or_create(name='Moderators')

        # Assign the user to the 'Moderators' group
        self.user.groups.add(moderators_group)

        # Create a Studio, Genre, and Anime for testing
        self.studio = Studio.objects.create(title='Studio 1')
        self.genre = Genre.objects.create(title='Genre 1')
        self.anime = Anime.objects.create(
            title='Test Anime',
            description='Test descriptionTest descriptionTest descriptionTest descriptionTest descriptionTest descriptionTest descriptionTest descriptionTest descriptionTest descriptionTest descriptionTest descriptionTest descriptionTest descriptionTest descriptionTest descriptionTest descriptionTest descriptionTest descriptionTest descriptionTest descriptionTest descriptionTest description',
            type='TV',
            episodes=12,
            ready_episodes=12,
            length_of_episodes=24,
            status='Ongoing',
            age_rating='PG-13',
            studio=self.studio,
            year=2022,
        )
        self.anime.genres.add(self.genre)

        # Set up the URL for the AnimeUpdateAPIView
        self.url = f'/catalog_api/anime-update/{self.anime.pk}/'

        # Set the Authorization header with the user's token (assuming you have authentication set up)
        self.token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_update_anime(self):
        # Update the anime data
        updated_data = {
            'title': 'Updated Anime',
            'description': 'Updated description Updated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated description',
            'type': 'Movie',
            'episodes': 24,
            'ready_episodes': 24,
            'length_of_episodes': 30,
            'status': 'Completed',
            'genres': ['Genre 1'],
            'age_rating': 'R',
            'studio': 'Studio 1',
            'year': 2023,
        }

        # Make a PUT request to update the Anime instance
        response = self.client.put(self.url, updated_data, format='json')
        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the anime instance from the database
        self.anime.refresh_from_db()

        # Check if the anime has been updated with the new data
        self.assertEqual(self.anime.title, 'Updated Anime')
        self.assertEqual(self.anime.description, 'Updated description Updated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated descriptionUpdated description')


class AnimeDeleteAPITest(APITestCase):
    def setUp(self):
        # Create a test user with necessary permissions
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Get or create the 'Moderators' group
        moderators_group, created = Group.objects.get_or_create(name='Moderators')

        # Assign the user to the 'Moderators' group
        self.user.groups.add(moderators_group)

        # Create a Studio, Genre, and Anime for testing
        self.studio = Studio.objects.create(title='Studio 1')
        self.genre = Genre.objects.create(title='Genre 1')
        self.anime = Anime.objects.create(
            title='Test Anime',
            description='Test description',
            type='TV',
            episodes=12,
            ready_episodes=12,
            length_of_episodes=24,
            status='Ongoing',
            age_rating='PG-13',
            studio=self.studio,
            year=2022,
        )
        self.anime.genres.add(self.genre)

        # Set up the URL for the AnimeDeleteAPIView
        self.url = f'/catalog_api/anime-delete/{self.anime.pk}/'

        # Set the Authorization header with the user's token (assuming you have authentication set up)
        self.token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_delete_anime(self):
        # Make a DELETE request to delete the Anime instance
        response = self.client.delete(self.url)

        # Check if the response status code is 204 No Content (indicating successful deletion)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Attempt to retrieve the deleted anime from the database
        deleted_anime = Anime.objects.filter(pk=self.anime.pk).first()

        # Check if the anime has been deleted (should be None)
        self.assertIsNone(deleted_anime)


class GenreListAPITest(APITestCase):
    def setUp(self):
        # Create some sample Genre objects for testing
        Genre.objects.create(title='Genre 1')
        Genre.objects.create(title='Genre 2')

    def test_genre_list(self):
        url = '/catalog_api/genre-list/'  # Update the URL if necessary

        # Make a GET request to the GenreListAPIView
        response = self.client.get(url)

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data contains the expected number of genres
        self.assertEqual(len(response.data), 2)  # Assuming you created two genres in the setup

        # Add more assertions to check the content of the response data if needed
        # For example, you can check if the titles of genres match the expected values
        self.assertEqual(response.data[0]['title'], 'Genre 1')
        self.assertEqual(response.data[1]['title'], 'Genre 2')


class GenreRetrieveAPITest(APITestCase):
    def setUp(self):
        # Create a sample Genre object for testing
        self.genre = Genre.objects.create(title='Test Genre')

    def test_genre_retrieve(self):
        url = f'/catalog_api/genre-retrieve/{self.genre.pk}/'  # Update the URL if necessary

        # Make a GET request to the GenreRetrieveAPIView
        response = self.client.get(url)

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data contains the expected details of the genre
        self.assertEqual(response.data['title'], 'Test Genre')

        # Add more assertions to check other details of the genre if needed
        # For example, you can check if the response data contains the genre's ID or other fields
        self.assertEqual(response.data['id'], self.genre.pk)


class GenreCreateAPITest(APITestCase):
    def setUp(self):
        # Create a test user with necessary permissions
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Get or create the 'Moderators' group
        moderators_group, created = Group.objects.get_or_create(name='Moderators')

        # Assign the user to the 'Moderators' group
        self.user.groups.add(moderators_group)

        # Set up the URL for the GenreCreateAPIView
        self.url = '/catalog_api/genre-create/'

        # Set the Authorization header with the user's token (assuming you have authentication set up)
        self.token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_genre(self):
        # Data for creating a new genre
        genre_data = {'title': 'New Genre'}

        # Make a POST request to create the new genre
        response = self.client.post(self.url, genre_data, format='json')

        # Check if the response status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the genre was actually created in the database
        created_genre = Genre.objects.filter(title='New Genre').first()
        self.assertIsNotNone(created_genre)


class GenreUpdateAPITest(APITestCase):
    def setUp(self):
        # Create a test user with necessary permissions
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Get or create the 'Moderators' group
        moderators_group, created = Group.objects.get_or_create(name='Moderators')

        # Assign the user to the 'Moderators' group
        self.user.groups.add(moderators_group)

        # Create a sample Genre object for testing
        self.genre = Genre.objects.create(title='Test Genre')

        # Set up the URL for the GenreUpdateAPIView
        self.url = f'/catalog_api/genre-update/{self.genre.pk}/'

        # Set the Authorization header with the user's token (assuming you have authentication set up)
        self.token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_update_genre(self):
        # Data for updating the existing genre
        updated_data = {'title': 'Updated Genre'}

        # Make a PUT request to update the existing genre
        response = self.client.put(self.url, updated_data, format='json')

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the genre instance from the database
        self.genre.refresh_from_db()

        # Check if the genre has been updated with the new data
        self.assertEqual(self.genre.title, 'Updated Genre')


class GenreDeleteAPITest(APITestCase):
    def setUp(self):
        # Create a test user with necessary permissions
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Get or create the 'Moderators' group
        moderators_group, created = Group.objects.get_or_create(name='Moderators')

        # Assign the user to the 'Moderators' group
        self.user.groups.add(moderators_group)

        # Create a sample Genre object for testing
        self.genre = Genre.objects.create(title='Test Genre')

        # Set up the URL for the GenreDeleteAPIView
        self.url = f'/catalog_api/genre-delete/{self.genre.pk}/'

        # Set the Authorization header with the user's token (assuming you have authentication set up)
        self.token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_delete_genre(self):
        # Make a DELETE request to delete the existing genre
        response = self.client.delete(self.url)

        # Check if the response status code is 204 No Content (indicating successful deletion)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Attempt to retrieve the deleted genre from the database
        deleted_genre = Genre.objects.filter(pk=self.genre.pk).first()

        # Check if the genre has been deleted (should be None)
        self.assertIsNone(deleted_genre)


class StudioListAPITest(APITestCase):
    def setUp(self):
        # Create some sample Studio objects for testing
        Studio.objects.create(title='Studio 1')
        Studio.objects.create(title='Studio 2')

    def test_studio_list(self):
        url = '/catalog_api/studio-list/'  # Update the URL if necessary

        # Make a GET request to the StudioListAPIView
        response = self.client.get(url)

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data contains the expected number of studios
        self.assertEqual(len(response.data), 2)  # Assuming you created two studios in the setup

        # Add more assertions to check the content of the response data if needed
        # For example, you can check if the titles of studios match the expected values
        self.assertEqual(response.data[0]['title'], 'Studio 1')
        self.assertEqual(response.data[1]['title'], 'Studio 2')


class StudioCreateAPITest(APITestCase):
    def setUp(self):
        # Create a test user with necessary permissions
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Get or create the 'Moderators' group
        moderators_group, created = Group.objects.get_or_create(name='Moderators')

        # Assign the user to the 'Moderators' group
        self.user.groups.add(moderators_group)

        # Set up the URL for the StudioCreateAPIView
        self.url = '/catalog_api/studio-create/'

        # Set the Authorization header with the user's token (assuming you have authentication set up)
        self.token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_studio(self):
        # Data for creating a new studio
        studio_data = {'title': 'New Studio'}

        # Make a POST request to create the new studio
        response = self.client.post(self.url, studio_data, format='json')

        # Check if the response status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the studio was actually created in the database
        created_studio = Studio.objects.filter(title='New Studio').first()
        self.assertIsNotNone(created_studio)


class StudioUpdateAPITest(APITestCase):
    def setUp(self):
        # Create a test user with necessary permissions
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Get or create the 'Moderators' group
        moderators_group, created = Group.objects.get_or_create(name='Moderators')

        # Assign the user to the 'Moderators' group
        self.user.groups.add(moderators_group)

        # Create a sample Studio object for testing
        self.studio = Studio.objects.create(title='Test Studio')

        # Set up the URL for the StudioUpdateAPIView
        self.url = f'/catalog_api/studio-update/{self.studio.pk}/'

        # Set the Authorization header with the user's token (assuming you have authentication set up)
        self.token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_update_studio(self):
        # Data for updating the existing studio
        updated_data = {'title': 'Updated Studio'}

        # Make a PUT request to update the existing studio
        response = self.client.put(self.url, updated_data, format='json')

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the studio instance from the database
        self.studio.refresh_from_db()

        # Check if the studio has been updated with the new data
        self.assertEqual(self.studio.title, 'Updated Studio')


class StudioDeleteAPITest(APITestCase):
    def setUp(self):
        # Create a test user with necessary permissions
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Get or create the 'Moderators' group
        moderators_group, created = Group.objects.get_or_create(name='Moderators')

        # Assign the user to the 'Moderators' group
        self.user.groups.add(moderators_group)

        # Create a sample Studio object for testing
        self.studio = Studio.objects.create(title='Test Studio')

        # Set up the URL for the StudioDeleteAPIView
        self.url = f'/catalog_api/studio-delete/{self.studio.pk}/'

        # Set the Authorization header with the user's token (assuming you have authentication set up)
        self.token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_delete_studio(self):
        # Make a DELETE request to delete the existing studio
        response = self.client.delete(self.url)

        # Check if the response status code is 204 No Content (indicating successful deletion)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Attempt to retrieve the deleted studio from the database
        deleted_studio = Studio.objects.filter(pk=self.studio.pk).first()

        # Check if the studio has been deleted (should be None)
        self.assertIsNone(deleted_studio)


class AnimeAverageRatingViewTest(APITestCase):
    def setUp(self):
        # Create a test user and profile
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        studio = Studio.objects.create(title='Studio 1')
        self.profile = Profile.objects.create(
            nickname='testuser',
            user=self.user,
            sex=Profile.MALE,
            birth_date=timezone.now().date(),
        )

        # Create a test anime
        self.anime = Anime.objects.create(
            title='Test Anime',
            description='Test description',
            type='TV',
            episodes=12,
            ready_episodes=12,
            length_of_episodes=24,
            status='Ongoing',
            age_rating='PG-13',
            year=2022,
            studio=studio,
        )

        # Create a test rating for the anime and user
        self.rating = Rating.objects.create(for_anime=self.anime, for_user=self.profile, rate=4)

        # Set up the URL for the AnimeAverageRatingView
        self.url = f'/catalog_api/anime-retrieve/{self.anime.pk}/average-rating/'

    def test_anime_average_rating(self):
        # Make a GET request to the AnimeAverageRatingView
        response = self.client.get(self.url)

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the expected average rating is in the response data
        self.assertIn('average_rating', response.data)

        # Add more assertions to check the content of the response data if needed
        # For example, you can check if the average rating matches the expected value
        self.assertEqual(response.data['average_rating'], '4.00')  # Adjust the expected value as needed


class AnimeRatingDistributionViewTest(APITestCase):
    def setUp(self):
        # Create a test user and profile
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        studio = Studio.objects.create(title='Studio 1')
        self.profile = Profile.objects.create(
            nickname='testuser',
            user=self.user,
            sex=Profile.MALE,
            birth_date=timezone.now().date(),
        )

        # Create a test anime
        self.anime = Anime.objects.create(
            title='Test Anime',
            description='Test description',
            type='TV',
            episodes=12,
            ready_episodes=12,
            length_of_episodes=24,
            status='Ongoing',
            age_rating='PG-13',
            year=2022,
            studio=studio,
        )

        # Create test ratings for the anime and user
        Rating.objects.create(for_anime=self.anime, for_user=self.profile, rate=4)

        # Set up the URL for the AnimeRatingDistributionView
        self.url = f'/catalog_api/anime-retrieve/{self.anime.pk}/rating-count/'

    def test_anime_rating_distribution(self):
        # Make a GET request to the AnimeRatingDistributionView
        response = self.client.get(self.url)

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the expected rating distribution is in the response data
        expected_distribution = {4: 1}  # Adjust the expected values based on your test data
        self.assertEqual(response.data, expected_distribution)


class UserRegistrationViewTest(APITestCase):
    def setUp(self):
        # Set up the URL for the UserRegistrationView
        self.url = "/catalog_api/register/"

        # Set up data for registration
        self.registration_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'nickname': 'TestUserNickname',
            'email': 'testuser@example.com',
            'bio': 'Test bio',
            'sex': 'male',
            'birth_date': '1990-01-01',
        }

    def test_user_registration(self):
        # Make a POST request to the UserRegistrationView with registration data
        response = self.client.post(self.url, self.registration_data, format='json')

        # Check if the response status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if a new user has been created in the database
        self.assertTrue(User.objects.filter(username='testuser').exists())

        # Optional: Check if the response contains access_token and refresh_token
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)


class RatingCreateAPIViewTest(APITestCase):
    def setUp(self):
        # Create a user with a profile for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        studio = Studio.objects.create(title='Studio 1')
        self.profile = Profile.objects.create(
            user=self.user,
            nickname='TestUser',
            birth_date='1990-06-06',
            sex='male',
            bio='',
        )

        # Create an anime for rating
        self.anime = Anime.objects.create(
            title='Test Anime',
            description='Test description',
            type='TV',
            episodes=12,
            ready_episodes=12,
            length_of_episodes=24,
            status='Ongoing',
            age_rating='PG-13',
            studio=studio,
            year=2022,
        )

        # Set up the URL for the RatingCreateAPIView
        self.url = "/catalog_api/rating-create/"

        # Generate a JWT access token
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_create_rating(self):
        # Prepare the data for rating creation
        data = {
            'for_anime': self.anime.title,
            'rate': 8,
        }

        # Include the JWT token in the Authorization header
        headers = {'Authorization': f'Bearer {self.access_token}'}

        # Make a POST request to the RatingCreateAPIView with token-based authentication
        response = self.client.post(self.url, data, format='json', headers=headers)

        # Check if the response status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if a new rating has been created in the database
        self.assertTrue(Rating.objects.filter(for_anime=self.anime, for_user=self.profile).exists())


class RatingUpdateAPIViewTest(APITestCase):
    def setUp(self):
        # Create a user with a profile for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        studio = Studio.objects.create(title='Studio 1')
        self.profile = Profile.objects.create(
            user=self.user,
            nickname='TestUser',
            birth_date='1990-06-06',
            sex='male',
            bio='',
        )

        # Create an anime and a rating for testing
        self.anime = Anime.objects.create(
            title='Test Anime',
            description='Test description',
            type='TV',
            episodes=12,
            ready_episodes=12,
            length_of_episodes=24,
            status='Ongoing',
            age_rating='PG-13',
            studio=studio,
            year=2022,
        )
        self.rating = Rating.objects.create(for_anime=self.anime, for_user=self.profile, rate=7)

        # Set up the URL for the RatingUpdateAPIView
        self.url = f"/catalog_api/rating-update/{self.rating.pk}/"

        # Generate a JWT access token
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_update_rating(self):
        # Prepare the data for rating update
        updated_rate = 9
        data = {
            'for_anime': self.anime.title,
            'rate': updated_rate,
        }

        # Include the JWT token in the Authorization header
        headers = {'Authorization': f'Bearer {self.access_token}'}

        # Make a PUT request to the RatingUpdateAPIView with token-based authentication
        response = self.client.put(self.url, data, format='json', headers=headers)

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the rating from the database
        self.rating.refresh_from_db()

        # Check if the rating has been updated with the new rate
        self.assertEqual(self.rating.rate, updated_rate)


class RatingDeleteAPIViewTest(APITestCase):
    def setUp(self):
        # Create a user with a profile for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        studio = Studio.objects.create(title='Studio 1')
        self.profile = Profile.objects.create(
            user=self.user,
            nickname='TestUser',
            birth_date='1990-06-06',
            sex='male',
            bio='',
        )

        # Create an anime and a rating for testing
        self.anime = Anime.objects.create(
            title='Test Anime',
            description='Test description',
            type='TV',
            episodes=12,
            ready_episodes=12,
            length_of_episodes=24,
            status='Ongoing',
            age_rating='PG-13',
            studio=studio,
            year=2022,
        )
        self.rating = Rating.objects.create(for_anime=self.anime, for_user=self.profile, rate=7)

        # Set up the URL for the RatingDeleteAPIView
        self.url = f"/catalog_api/rating-delete/{self.rating.pk}/"

        # Generate a JWT access token
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_delete_rating(self):
        # Include the JWT token in the Authorization header
        headers = {'Authorization': f'Bearer {self.access_token}'}

        # Make a DELETE request to the RatingDeleteAPIView with token-based authentication
        response = self.client.delete(self.url, format='json', headers=headers)

        # Check if the response status code is 204 No Content (indicating successful deletion)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check if the rating has been deleted from the database
        self.assertFalse(Rating.objects.filter(pk=self.rating.pk).exists())


class CollectionListAPIViewTest(APITestCase):
    def setUp(self):
        # Create a user with a profile for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        studio = Studio.objects.create(title='Studio 1')
        self.profile = Profile.objects.create(
            user=self.user,
            nickname='TestUser',
            birth_date='1990-06-06',
            sex='male',
            bio='',
        )

        # Create an anime and a collection for testing
        self.anime = Anime.objects.create(
            title='Test Anime',
            description='Test description',
            type='TV',
            episodes=12,
            ready_episodes=12,
            length_of_episodes=24,
            status='Ongoing',
            age_rating='PG-13',
            studio=studio,
            year=2022,
        )
        self.collection = Collection.objects.create(name='Test Collection', user=self.profile)
        self.collection.items.add(self.anime)

        # Set up the URL for the CollectionListAPIView
        self.url = "/catalog_api/collection-list/"

        # Generate a JWT access token
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_get_collection_list(self):
        # Include the JWT token in the Authorization header
        headers = {'Authorization': f'Bearer {self.access_token}'}

        # Make a GET request to the CollectionListAPIView with token-based authentication
        response = self.client.get(self.url, format='json', headers=headers)

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response contains the expected collection data
        self.assertEqual(response.data[0]['name'], 'Test Collection')
        self.assertEqual(response.data[0]['items'][0], 'Test Anime')


class CollectionCreateAPIViewTest(APITestCase):
    def setUp(self):
        # Create a user with a profile for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        studio = Studio.objects.create(title='Studio 1')
        self.profile = Profile.objects.create(
            user=self.user,
            nickname='TestUser',
            birth_date='1990-06-06',
            sex='male',
            bio='',
        )

        self.anime = Anime.objects.create(
            title='Test Anime',
            description='Test description',
            type='TV',
            episodes=12,
            ready_episodes=12,
            length_of_episodes=24,
            status='Ongoing',
            age_rating='PG-13',
            studio=studio,
            year=2022,
        )

        # Set up the URL for the CollectionCreateAPIView
        self.url = "/catalog_api/collection-create/"

        # Set up data for creating a new collection
        self.collection_data = {
            'name': 'New Collection',
            'items': [self.anime.title],
        }

        # Generate a JWT access token
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_create_collection(self):
        # Include the JWT token in the Authorization header
        headers = {'Authorization': f'Bearer {self.access_token}'}

        # Make a POST request to the CollectionCreateAPIView with token-based authentication
        response = self.client.post(self.url, self.collection_data, format='json', headers=headers)

        # Check if the response status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if a new collection has been created in the database
        self.assertTrue(Collection.objects.filter(name='New Collection').exists())

        # Optional: Check if the response contains the expected collection data
        self.assertEqual(response.data['name'], 'New Collection')
        self.assertEqual(response.data['items'][0], 'Test Anime')


class CollectionUpdateAPIViewTest(APITestCase):
    def setUp(self):
        # Create a user with a profile for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        studio = Studio.objects.create(title='Studio 1')
        self.profile = Profile.objects.create(
            user=self.user,
            nickname='TestUser',
            birth_date='1990-06-06',
            sex='male',
            bio='',
        )

        self.anime = Anime.objects.create(
            title='Test Anime',
            description='Test description',
            type='TV',
            episodes=12,
            ready_episodes=12,
            length_of_episodes=24,
            status='Ongoing',
            age_rating='PG-13',
            studio=studio,
            year=2022,
        )
        self.collection = Collection.objects.create(name='Test Collection', user=self.profile)
        self.collection.items.add(self.anime)

        # Set up the URL for the CollectionUpdateAPIView
        self.url = f"/catalog_api/collection-update/{self.collection.id}/"

        # Set up data for updating the collection
        self.updated_collection_data = {
            'name': 'Updated Collection',
            'items': [self.anime.title],  # Updated list of anime items
        }

        # Generate a JWT access token
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_update_collection(self):
        # Include the JWT token in the Authorization header
        headers = {'Authorization': f'Bearer {self.access_token}'}

        # Make a PUT request to the CollectionUpdateAPIView with token-based authentication
        response = self.client.put(self.url, self.updated_collection_data, format='json', headers=headers)

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the collection in the database has been updated
        updated_collection = Collection.objects.get(id=self.collection.id)
        self.assertEqual(updated_collection.name, 'Updated Collection')

        # Optional: Check if the response contains the expected updated collection data
        self.assertEqual(response.data['name'], 'Updated Collection')
        self.assertEqual(response.data['items'][0], 'Test Anime')


class CollectionDeleteAPIViewTest(APITestCase):
    def setUp(self):
        # Create a user with a profile for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        studio = Studio.objects.create(title='Studio 1')
        self.profile = Profile.objects.create(
            user=self.user,
            nickname='TestUser',
            birth_date='1990-06-06',
            sex='male',
            bio='',
        )

        self.anime = Anime.objects.create(
            title='Test Anime',
            description='Test description',
            type='TV',
            episodes=12,
            ready_episodes=12,
            length_of_episodes=24,
            status='Ongoing',
            age_rating='PG-13',
            studio=studio,
            year=2022,
        )
        self.collection = Collection.objects.create(name='Test Collection', user=self.profile)
        self.collection.items.add(self.anime)

        # Set up the URL for the CollectionDeleteAPIView
        self.url = f"/catalog_api/collection-delete/{self.collection.id}/"

        # Generate a JWT access token
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_delete_collection(self):
        # Include the JWT token in the Authorization header
        headers = {'Authorization': f'Bearer {self.access_token}'}

        # Make a DELETE request to the CollectionDeleteAPIView with token-based authentication
        response = self.client.delete(self.url, headers=headers)

        # Check if the response status code is 204 No Content (indicating successful deletion)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check if the collection has been deleted from the database
        with self.assertRaises(Collection.DoesNotExist):
            Collection.objects.get(id=self.collection.id)

        # Optional: Check if the response contains the expected data (empty since it's a delete request)
        self.assertEqual(response.data, None)


class CommentListAPIViewTest(APITestCase):
    def setUp(self):
        # Create a user with a profile for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        studio = Studio.objects.create(title='Studio 1')
        self.profile = Profile.objects.create(
            user=self.user,
            nickname='TestUser',
            birth_date='1990-06-06',
            sex='male',
            bio='',
        )

        self.anime = Anime.objects.create(
            title='Test Anime',
            description='Test description',
            type='TV',
            episodes=12,
            ready_episodes=12,
            length_of_episodes=24,
            status='Ongoing',
            age_rating='PG-13',
            studio=studio,
            year=2022,
        )

        # Create comments for the anime
        self.comment1 = Comment.objects.create(user=self.profile, anime=self.anime, text='Comment 1')
        self.comment2 = Comment.objects.create(user=self.profile, anime=self.anime, text='Comment 2', parent=self.comment1)

        # Set up the URL for the CommentListAPIView
        self.url = f"/catalog_api/comment-list/"

        # Generate a JWT access token
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_get_comment_list(self):
        # Include the JWT token in the Authorization header
        headers = {'Authorization': f'Bearer {self.access_token}'}

        # Make a GET request to the CommentListAPIView with token-based authentication
        response = self.client.get(self.url, headers=headers)

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data contains the expected comments
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['text'], 'Comment 1')
        self.assertEqual(response.data[1]['text'], 'Comment 2')


class CommentCreateAPIViewTest(APITestCase):
    def setUp(self):
        # Create a user with a profile for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        studio = Studio.objects.create(title='Studio 1')
        self.profile = Profile.objects.create(
            user=self.user,
            nickname='TestUser',
            birth_date='1990-06-06',
            sex='male',
            bio='',
        )

        self.anime = Anime.objects.create(
            title='Test Anime',
            description='Test description',
            type='TV',
            episodes=12,
            ready_episodes=12,
            length_of_episodes=24,
            status='Ongoing',
            age_rating='PG-13',
            studio=studio,
            year=2022,
        )

        # Set up the URL for the CommentCreateAPIView
        self.url = f"/catalog_api/comment-create/"

        # Generate a JWT access token
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_create_comment(self):
        # Include the JWT token in the Authorization header
        headers = {'Authorization': f'Bearer {self.access_token}'}

        # Set up data for creating a new comment
        comment_data = {
            'text': 'New Comment',
            'anime': self.anime.id,
            'parent': None  # Set to the parent comment ID if it's a reply
        }

        # Make a POST request to the CommentCreateAPIView with token-based authentication
        response = self.client.post(self.url, comment_data, headers=headers, format='json')

        # Check if the response status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if a new comment has been created in the database
        self.assertTrue(Comment.objects.filter(text=response.data['text']).exists())


class CommentUpdateAPIViewTest(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        studio = Studio.objects.create(title='Studio 1')
        self.profile = Profile.objects.create(
            user=self.user,
            nickname='TestUser',
            birth_date='1990-06-06',
            sex='male',
            bio='',
        )

        self.anime = Anime.objects.create(
            title='Test Anime',
            description='Test description',
            type='TV',
            episodes=12,
            ready_episodes=12,
            length_of_episodes=24,
            status='Ongoing',
            age_rating='PG-13',
            studio=studio,
            year=2022,
        )

        # Create a comment
        self.comment = Comment.objects.create(
            user=self.profile,  # Assuming you have a profile attribute on your User model
            anime=self.anime,
            text='Test comment',
        )

        # Set up the URL for the CommentUpdateAPIView
        self.url = f'/catalog_api/comment-update/{self.comment.pk}/'

    def test_update_comment_by_owner(self):
        updated_text = 'Updated comment text'
        data = {'text': updated_text, 'anime': self.anime.id}

        # Make a PUT request to update the comment
        # Authenticate the user
        self.token = str(AccessToken.for_user(self.user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.put(self.url, data, format='json')

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the comment has been updated in the database
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.text, updated_text)

    def test_update_comment_by_non_owner(self):
        # Create another user
        another_user = User.objects.create_user(username='anotheruser', password='anotherpassword')

        # Authenticate the other user
        self.token = str(AccessToken.for_user(another_user))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Try to update the comment as a non-owner
        response = self.client.put(self.url, {'text': 'Attempt to update as non-owner'}, format='json')

        # Check if the response status code is 403 Forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Check if the comment text remains unchanged
        self.comment.refresh_from_db()
        self.assertNotEqual(self.comment.text, 'Attempt to update as non-owner')


class CommentDeleteAPIViewTest(APITestCase):
    def setUp(self):
        # Assuming you have a user object created in your setup
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        studio = Studio.objects.create(title='Studio 1')
        self.profile = Profile.objects.create(
            user=self.user,
            nickname='TestUser',
            birth_date='1990-06-06',
            sex='male',
            bio='',
        )

        self.anime = Anime.objects.create(
            title='Test Anime',
            description='Test description',
            type='TV',
            episodes=12,
            ready_episodes=12,
            length_of_episodes=24,
            status='Ongoing',
            age_rating='PG-13',
            studio=studio,
            year=2022,
        )

        self.comment = Comment.objects.create(
            user=self.profile,
            anime=self.anime,
            text='Test Comment')

    # def get_access_token(self, user):
    #     refresh = RefreshToken.for_user(user)
    #     return str(refresh.access_token)

    def test_comment_delete(self):
        # Authenticate the user and get the access token
        access_token = str(AccessToken.for_user(self.user))

        # Make a request with the access token in the Authorization header
        response = self.client.delete(f'/catalog_api/comment-delete/{self.comment.pk}/', HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Your assertion checks here
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Optional: Check if the comment is deleted from the database
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())


class CommentRetrieveAPIViewTest(APITestCase):
    def setUp(self):
        # Assuming you have a Comment object created in your setup
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        studio = Studio.objects.create(title='Studio 1')
        self.profile = Profile.objects.create(
            user=self.user,
            nickname='TestUser',
            birth_date='1990-06-06',
            sex='male',
            bio='',
        )

        self.anime = Anime.objects.create(
            title='Test Anime',
            description='Test description',
            type='TV',
            episodes=12,
            ready_episodes=12,
            length_of_episodes=24,
            status='Ongoing',
            age_rating='PG-13',
            studio=studio,
            year=2022,
        )
        self.comment = Comment.objects.create(
            user=self.profile,
            anime=self.anime,
            text='Test Comment')

    def test_comment_retrieve(self):
        # Make a GET request to retrieve the comment
        response = self.client.get(f'/catalog_api/comment-retrieve/{self.comment.pk}/')

        # Your assertion checks here
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], 'Test Comment')  # Adjust this based on your serializer fields


class ReviewRetrieveAPIViewTest(APITestCase):
    def setUp(self):
        # Assuming you have a Review object created in your setup
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        studio = Studio.objects.create(title='Studio 1')
        self.profile = Profile.objects.create(
            user=self.user,
            nickname='TestUser',
            birth_date='1990-06-06',
            sex='male',
            bio='',
        )

        self.anime = Anime.objects.create(
            title='Test Anime',
            description='Test description',
            type='TV',
            episodes=12,
            ready_episodes=12,
            length_of_episodes=24,
            status='Ongoing',
            age_rating='PG-13',
            studio=studio,
            year=2022,
        )
        self.review = Review.objects.create(
            anime=self.anime,
            storyline=5,
            characters=4,
            artwork=5,
            sound_series=4,
            final_grade=4,
            text='Test Review',
            user=self.profile,
        )

    def test_review_retrieve(self):
        # Make a GET request to retrieve the review
        response = self.client.get(f'/catalog_api/review-retrieve/{self.review.pk}/')

        # Your assertion checks here
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], 'Test Review')  # Adjust this based on your serializer fields


class ReviewListAPIViewTest(APITestCase):
    def setUp(self):
        # Assuming you have some Review objects created in your setup
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        studio = Studio.objects.create(title='Studio 1')
        self.profile = Profile.objects.create(
            user=self.user,
            nickname='TestUser',
            birth_date='1990-06-06',
            sex='male',
            bio='',
        )

        self.anime = Anime.objects.create(
            title='Test Anime',
            description='Test description',
            type='TV',
            episodes=12,
            ready_episodes=12,
            length_of_episodes=24,
            status='Ongoing',
            age_rating='PG-13',
            studio=studio,
            year=2022,
        )
        self.anime1 = Anime.objects.create(
            title='Test Anime1',
            description='Test description1',
            type='TV',
            episodes=12,
            ready_episodes=12,
            length_of_episodes=24,
            status='Ongoing',
            age_rating='PG-13',
            studio=studio,
            year=2021,
        )
        self.review1 = Review.objects.create(
            anime=self.anime,
            storyline=5,
            characters=4,
            artwork=5,
            sound_series=4,
            final_grade=4,
            text='Test Review 1',
            user=self.profile,
        )
        self.review2 = Review.objects.create(
            anime=self.anime1,
            storyline=3,
            characters=5,
            artwork=4,
            sound_series=5,
            final_grade=5,
            text='Test Review 2',
            user=self.profile,
        )

    def test_review_list_with_anime_filter(self):
        # Make a GET request to the ReviewListAPIView with anime filter
        response = self.client.get('/catalog_api/review-list/', {'anime': 'Test Anime'})

        # Your assertion checks here
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Adjust based on your expected result
        self.assertEqual(response.data[0]['text'], 'Test Review 1')  # Adjust this based on your serializer fields

        # Optional: Add more assertions based on your serializer fields and expected data

    def test_review_list_without_filter(self):
        # Make a GET request to the ReviewListAPIView without any filter
        response = self.client.get('/catalog_api/review-list/')

        # Your assertion checks here
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Adjust based on your expected result


class ReviewCreateAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        studio = Studio.objects.create(title='Studio 1')
        self.user_profile = Profile.objects.create(
            user=self.user,
            nickname='TestUser',
            birth_date='1990-06-06',
            sex='male',
            bio='',
        )

        self.anime = Anime.objects.create(
            title='Test Anime',
            description='Test description',
            type='TV',
            episodes=12,
            ready_episodes=12,
            length_of_episodes=24,
            status='Ongoing',
            age_rating='PG-13',
            studio=studio,
            year=2022,
        )

        # Authenticated user token setup
        self.token = str(AccessToken.for_user(self.user))

        # Your Review data for POST request
        self.review_data = {
            'user': self.user_profile.id,
            'anime': 'Test Anime',
            'storyline': 4,
            'characters': 5,
            'artwork': 4,
            'sound_series': 5,
            'final_grade': 5,
            'text': 'Test ReviewTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest Anime',
        }

    def test_create_review_authenticated_user(self):
        # Set Authorization header with the token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Make a POST request to the ReviewCreateAPIView with review data
        response = self.client.post('/catalog_api/review-create/', self.review_data, format='json')

        # Your assertion checks here
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)  # Assuming only one review is created
        self.assertEqual(Review.objects.first().text, 'Test ReviewTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest AnimeTest Anime')  # Adjust based on your expected result

    def test_create_review_unauthenticated_user(self):
        # Make a POST request to the ReviewCreateAPIView without Authorization header
        response = self.client.post('/catalog_api/review-create/', self.review_data, format='json')

        # Your assertion checks here
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Review.objects.count(), 0)  # No review should be created


class ReviewUpdateAPIViewTest(APITestCase):
    def setUp(self):
        # Assuming you have an Anime instance, Profile instance, and Review instance created in your setup
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        studio = Studio.objects.create(title='Studio 1')
        self.user_profile = Profile.objects.create(
            user=self.user,
            nickname='TestUser',
            birth_date='1990-06-06',
            sex='male',
            bio='',
        )

        self.anime = Anime.objects.create(
            title='Test Anime',
            description='Test description',
            type='TV',
            episodes=12,
            ready_episodes=12,
            length_of_episodes=24,
            status='Ongoing',
            age_rating='PG-13',
            studio=studio,
            year=2022,
        )

        self.review = Review.objects.create(
            anime=self.anime,
            storyline=4,
            characters=5,
            artwork=4,
            sound_series=5,
            final_grade=5,
            text='Test ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest Review',
            user=self.user_profile
        )

        # Authenticated user token setup
        self.token = str(AccessToken.for_user(self.user))

        # Your updated Review data for PUT request
        self.updated_review_data = {
            'anime': 'Test Anime',
            'storyline': 3,
            'characters': 4,
            'artwork': 3,
            'sound_series': 4,
            'final_grade': 4,
            'text': 'Updated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review Text',
        }

    def test_update_review_authenticated_user(self):
        # Set Authorization header with the token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Make a PUT request to the ReviewUpdateAPIView with updated review data
        response = self.client.put(f'/catalog_api/review-update/{self.review.pk}/', self.updated_review_data, format='json')

        # Your assertion checks here
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()  # Refresh the instance to get the latest data from the database
        self.assertEqual(self.review.text, 'Updated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review TextUpdated Review Text')  # Adjust based on your expected result

    def test_update_review_unauthenticated_user(self):
        # Make a PUT request to the ReviewUpdateAPIView without Authorization header
        response = self.client.put(f'/catalog_api/review-update/{self.review.pk}/', self.updated_review_data, format='json')

        # Your assertion checks here
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.review.refresh_from_db()  # Ensure the review remains unchanged
        self.assertEqual(self.review.text, 'Test ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest Review')  # Adjust based on your expected result


class ReviewDeleteAPIViewTest(APITestCase):
    def setUp(self):
        # Assuming you have an Anime instance, Profile instance, and Review instance created in your setup
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        studio = Studio.objects.create(title='Studio 1')
        self.user_profile = Profile.objects.create(
            user=self.user,
            nickname='TestUser',
            birth_date='1990-06-06',
            sex='male',
            bio='',
        )

        self.anime = Anime.objects.create(
            title='Test Anime',
            description='Test description',
            type='TV',
            episodes=12,
            ready_episodes=12,
            length_of_episodes=24,
            status='Ongoing',
            age_rating='PG-13',
            studio=studio,
            year=2022,
        )
        self.review = Review.objects.create(
            anime=self.anime,
            storyline=4,
            characters=5,
            artwork=4,
            sound_series=5,
            final_grade=5,
            text='Test ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest ReviewTest Review',
            user=self.user_profile
        )

        # Authenticated user token setup
        self.token = str(AccessToken.for_user(self.user))

    def test_delete_review_authenticated_user(self):
        # Set Authorization header with the token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Make a DELETE request to the ReviewDeleteAPIView
        response = self.client.delete(f'/catalog_api/review-delete/{self.review.pk}/')

        # Your assertion checks here
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Review.DoesNotExist):
            self.review.refresh_from_db()  # Attempting to refresh should raise DoesNotExist

    def test_delete_review_unauthenticated_user(self):
        # Make a DELETE request to the ReviewDeleteAPIView without Authorization header
        response = self.client.delete(f'/catalog_api/review-delete/{self.review.pk}/')

        # Your assertion checks here
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.review.refresh_from_db()
