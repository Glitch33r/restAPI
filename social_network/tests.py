import json
from pprint import pprint
import random

from django.contrib.auth.models import User
from rest_framework import status
from django.test import TestCase
from django.urls import reverse

from social_network.models import Post
from social_network.serializers import PostListSerializer, PostDetailSerializer, PostLikeUnLikeSerializer

USER_DATA = {
    'username': 'user_for_test',
    'email': 'info@foxtrot.com.ua',
    'password': 'Q2w3e4r%'
}


class PostTest(TestCase):
    def setUp(self) -> None:
        response = self.client.post(
            reverse('social_network:sign-up'),
            data=json.dumps(USER_DATA),
            content_type='application/json'
        )
        temp = response.data.get('tokens')
        self.token = temp['access']
        self.refresh = temp['refresh']

        self.client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {self.token}'

        self.post1 = Post.objects.create(
            name='test1',
            text='test1',
            author=User.objects.get(username=USER_DATA['username'])
        )
        self.post2 = Post.objects.create(
            name='test2',
            text='test2',
            author=User.objects.get(username=USER_DATA['username'])
        )
        self.post3 = Post.objects.create(
            name='test3',
            text='test3',
            author=User.objects.get(username=USER_DATA['username'])
        )

        self.client.post(
            reverse('social_network:login'),
            data=json.dumps({'username': 'user_for_test', 'password': 'Q2w3e4r%'}),
            content_type='application/json'
        )

    def test_post_create(self):
        response = self.client.post(
            reverse('social_network:post-create'),
            data={
                "name": "test4",
                "text": "test4"
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_list(self):
        response = self.client.get(
            reverse('social_network:post-list'),
            content_type='application/json'
        )
        posts = Post.objects.all()
        serializer = PostListSerializer(posts, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_detail(self):
        ids = [post.id for post in Post.objects.all()]
        post = random.choice(ids)
        response = self.client.get(
            reverse('social_network:post-detail', kwargs={'pk': post}),
            content_type='application/json'
        )
        serializer = PostDetailSerializer(Post.objects.get(id=post))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_delete(self):
        response = self.client.delete(
            reverse('social_network:post-detail', kwargs={'pk': self.post1.id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_post_edit(self):
        response = self.client.put(
            reverse('social_network:post-detail', kwargs={'pk': self.post3.id}),
            data={
                "name": "test3_3",
                "text": "test3_3"
            },
            content_type='application/json'
        )
        post = Post.objects.get(name="test3_3")
        serializer = PostDetailSerializer(post)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_like(self):
        for _ in range(0, 2):
            response = self.client.patch(
                reverse('social_network:post-interactive', kwargs={'pk': self.post2.id, 'type': 'like'}),
                content_type='application/json'
            )

        post = Post.objects.get(id=self.post2.id)
        serializer = PostLikeUnLikeSerializer(post)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_unlike(self):
        for _ in range(0, 3):
            response = self.client.patch(
                reverse('social_network:post-interactive', kwargs={'pk': self.post2.id, 'type': 'unlike'}),
                content_type='application/json'
            )

        post = Post.objects.get(id=self.post2.id)
        serializer = PostLikeUnLikeSerializer(post)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserLoginTest(TestCase):
    def setUp(self) -> None:
        User.objects.create_user('user_for_test', 'info@foxtrot.com.ua', 'Q2w3e4r%')

    def test_user_login(self):
        response = self.client.post(
            reverse('social_network:login'),
            data=json.dumps({'username': 'user_for_test', 'password': 'Q2w3e4r%'}),
            content_type='application/json'
        )
        pprint(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserSignUpTest(TestCase):
    def setUp(self) -> None:
        self.valid_user_data = USER_DATA

        self.invalid_user_data = {
            'username': 'user_for_test_',
            'email': 'info@fo.com.ua',
            'password': 'Q2w3e4r%'
        }

    def test_valid_sign_up(self):
        response = self.client.post(
            reverse('social_network:sign-up'),
            data=json.dumps(self.valid_user_data),
            content_type='application/json'
        )
        pprint(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_sign_up(self):
        response = self.client.post(
            reverse('social_network:sign-up'),
            data=json.dumps(self.invalid_user_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
