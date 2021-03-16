import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from search.models import User
from search.serializer import SearchUsersSerializer, UserSerializer

client = Client()


class GetAllUsersTest(TestCase):
    """ Test module for GET all users API """
    def setUp(self):
        User.objects.create(name='Casper', x=0, y=1, description="Some text")
        User.objects.create(name='Casper_1', x=4, y=1, description="Some text")
        User.objects.create(name='Casper_2', x=3, y=2, description="Some text")
        User.objects.create(name='Casper_3', x=1, y=10, description="Some text")

    def test_get_all_users(self):
        # get API response
        response = client.get(reverse('search:get_all_users'))
        # get data from db
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data['users'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleUserTest(TestCase):
    """ Test module for GET single users API """
    def setUp(self):
        self.casper = User.objects.create(name='Casper', x=3, y=4, description="Some text!")
        self.casper_1 = User.objects.create(name='Casper1', x=1, y=4, description="Some text!")
        self.casper_2 = User.objects.create(name='Casper2', x=3, y=2, description="Some text!")
        self.casper_3 = User.objects.create(name='Casper3', x=3, y=3, description="Some text!")
        self.casper_4 = User.objects.create(name='Casper4', x=3, y=0, description="Some text!")

    def test_get_valid_single_puppy(self):
        response = client.get(
            reverse('search:get_id_user', kwargs={'pk': self.casper.pk}))
        user = User.objects.get(pk=self.casper.pk)
        serializer = UserSerializer(user)
        self.assertEqual(response.data['user'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_puppy(self):
        response = client.get(
            reverse('search:get_id_user', kwargs={'pk': 105}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewUserTest(TestCase):
    """ Test module for inserting a new puppy """
    def setUp(self):
        self.valid_payload = {
            'name': 'Muffin',
            'x': 5,
            'y': 3,
            'description': "Some comment!"
        }
        self.invalid_payload = {
            'name': '',
            'x': 5,
            'y': 3,
            'description': "Some comment!"
        }

    def test_create_valid_puppy(self):
        response = client.post(
            reverse('search:get_all_users'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_puppy(self):
        response = client.post(
            reverse('search:get_all_users'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleUserTest(TestCase):
    """ Test module for updating an existing puppy record """
    def setUp(self):
        self.casper = User.objects.create(name='Casper', x=3, y=4, description="Some text!")
        self.casper_1 = User.objects.create(name='Casper1', x=1, y=4, description="Some text!")
        self.valid_payload = {
            'name': 'Muffin',
            'x': 5,
            'y': 3,
            'description': "Some comment!"
        }
        self.invalid_payload = {
            'name': '',
            'x': 5,
            'y': 3,
            'description': "Some comment!"
        }

    def test_valid_update_puppy(self):
        response = client.put(
            reverse('search:get_id_user', kwargs={'pk': self.casper.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_puppy(self):
        response = client.put(
            reverse('search:get_id_user', kwargs={'pk': self.casper_1.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleUserTest(TestCase):
    """ Test module for deleting an existing puppy record """
    def setUp(self):
        self.casper = User.objects.create(name='Casper', x=3, y=4, description="Some text!")
        self.casper_1 = User.objects.create(name='Casper1', x=1, y=4, description="Some text!")

    def test_valid_delete_puppy(self):
        response = client.delete(
            reverse('search:get_id_user', kwargs={'pk': self.casper.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_puppy(self):
        response = client.delete(
            reverse('search:get_id_user', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


"""class SearchUsersTest(TestCase):

    def setUp(self):
        User.objects.create(name='Casper', x=301, y=301, description="Some text!")
        User.objects.create(name='Casper1', x=302, y=304, description="Some text!")
        User.objects.create(name='Casper2', x=303, y=302, description="Some text!")
        User.objects.create(name='Casper3', x=304, y=300, description="Some text!")
        User.objects.create(name='Casper4', x=305, y=303, description="Some text!")
        self.payload_2 = {
            'x': 300,
            'y': 300,
            'k': 2,
            'm': 10
        }
        self.payload_3 = {
            'x': 300,
            'y': 300,
            'k': 3,
            'm': 10
        }
        self.payload_0 = {
            'x': 400,
            'y': 400,
            'k': 2,
            'm': 1
        }

    def test_valid_2(self):
        response = client.get(
            reverse('search:get_search_users'),
            data=json.dumps(self.payload_2),
            content_type='application/json'
        )
        users = User.objects.filter(x__lte=(self.payload_2["x"] + self.payload_2["m"]),
                                    y__lte=(self.payload_2['y'] + self.payload_2["m"]))
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_3(self):
        print(json.dumps(self.payload_3))
        response = client.get(
            reverse('search:get_search_users'),
            data=json.dumps(self.payload_3),
            content_type='application/json'
        )
        users = User.objects.filter(x__lte=(self.payload_3["x"] + self.payload_3["m"]),
                                    y__lte=(self.payload_3['y'] + self.payload_3["m"]))
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data['users'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_0(self):
        response = client.get(
            reverse('search:get_search_users'),
            data=self.payload_0,
            content_type='application/json'
        )
        users = User.objects.filter(x__lte=(self.payload_0["x"] + self.payload_0["m"]),
                                    y__lte=(self.payload_0['y'] + self.payload_0["m"]))
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)"""
