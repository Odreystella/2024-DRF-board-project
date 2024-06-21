"""
1. 게시글 목록 - 인증되지 않은 상태에서 요청할 수 있음
    - GET /api/v1/posts
    - GET /api/v1/posts?page=1&ordering=view_count
    - GET /api/v1/posts?page=1&ordering=created_at
    - return 제목, 사용자 이름, 조회수
    - 토큰이 없어도 목록이 조회되는 성공 케이스
    - limit, offset의 디폴트는 10, 0 으로 갯수가 10개인지 보여주는 케이스, 데이터가 10개 미만일 수 있음.
    - 탈퇴한 유저의 글인 포함된 경우, 사용자 이름이 '탈퇴한 유저'라고 보여지는 케이스

2. 게시글 생성 - 인증된 상태에서 요청할 수 있음
    - POST /api/v1/posts
    - jwt토큰으로 게시글 생성 성공 케이스
    - 토큰이 없으면 401 에러
    - 제목과 내용이 없으면 EmptyInputException
    - 제목이 100자 이상이면 Over100ContentException

3. 게시글 조회 - 인증되지 않은 상태에서 요청할 수 있음
    - GET /api/v1/posts/{post_id}
    - return 제목, 내용, 사용자 이름, 작성시간, 수정시간(수정되지 않았다면 빈값..)
    - 토큰 없어도 게시글 조회하는 성공 케이스
    - 요청이 들어올떄마다 view_count가 1 증가하는지 확인하는 케이스
    - 탈퇴한 유저의 글인 경우, 사용자 이름이 '탈퇴한 유저'라고 보여지는 케이스

4. 게시글 수정 - 인증된 상태에서 요청할 수 있음
    - PUT /api/v1/posts/{post_id}
    - jwt토큰으로 게시글 제목이나 내용 수정 케이스
    - jwt토큰의 유저와 게시글 작성 유저가 다를 경우 에러 케이스 IsNotMe

5. 게시글 삭제 - 인증된 상태에서 요청할 수 있음
    - DELETE /api/v1/posts/{post_id}
    - jwt토큰으로 게시글 삭제 케이스
    - jwt토큰의 유저와 게시글 작성 유저가 다를 경우 에러 케이스 IsNotMe
"""

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import (
    APITestCase,
    APIClient,
)
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import Post


POST_URL = reverse('posts:list_and_create')


class PublicPostApiTests(APITestCase):
    """
    인증이 필요하지 않는 APIs 테스트.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            name="Test",
            email="test@example.com",
            password="Test1234!",
        )
        self.post = Post.objects.create(
            title='This is title.',
            content='This is content',
            user=self.user
        )

    def test_get_post_list_without_jwt_success(self):
        """
        return 제목, 사용자 이름, 조회수
        토큰이 없어도 목록이 조회되는 성공 케이스
        """
        res = self.client.get(POST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_post_detail_without_jwt_success(self):
        """
        return 제목, 내용, 사용자 이름, 작성시간, 수정시간(수정되지 않았다면 빈값..)
        토큰 없어도 게시글 조회하는 성공 케이스
        """
        POST_DETAIL_URL = reverse('posts:detail', kwargs={'pk': self.post.pk})

        res = self.client.get(POST_DETAIL_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_increase_view_count_success(self):
        """
        요청이 들어올떄마다 view_count가 1 증가하는지 확인하는 케이스
        """
        POST_DETAIL_URL = reverse('posts:detail', kwargs={'pk': self.post.pk})

        self.assertEqual(self.post.view_count, 0)

        res = self.client.get(POST_DETAIL_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.view_count, 1)

        res = self.client.get(POST_DETAIL_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.view_count, 2)

    def test_inactive_user_name_check(self):
        """
        탈퇴한 유저의 글인 경우, 사용자 이름이 '탈퇴한 유저'라고 보여지는 케이스
        """
        user = get_user_model().objects.create_user(
            name="Test2",
            email="test2@example.com",
            password="Test1234!",
            is_deleted=True
        )
        post = Post.objects.create(
            title='This is title.',
            content='This is content',
            user=user
        )
        POST_DETAIL_URL = reverse('posts:detail', kwargs={'pk': post.pk})

        res = self.client.get(POST_DETAIL_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['creator'], '탈퇴한 유저')


class PrivatePostApiTests(APITestCase):
    """
    인증이 필요한 APIs 테스트.
    """
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            name="Test",
            email="test@example.com",
            password="Test1234!",
        )
        self.post = Post.objects.create(
                title='This is title',
                content='This is content',
                user=self.user
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

    def test_create_new_post_with_jwt_success(self):
        """
        jwt토큰으로 게시글 생성 성공 케이스
        """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        payload = {
            'title': 'This is title',
            'content': 'This is content',
        }
        res = self.client.post(POST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


    def test_new_post_not_create_without_jwt_error(self):
        """
        토큰이 없으면 401 에러 케이스.
        """
        payload = {
            'title': 'This is title',
            'content': 'This is content',
        }
        res = self.client.post(POST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_new_post_not_create_with_empty_input_error(self):
        """
        제목과 내용이 없으면 EmptyInputException.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        payload = {
            'title': '',
            'content': 'This is content',
        }
        res = self.client.post(POST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_new_post_not_create_with_over_100_title_error(self):
        """
        제목이 100자 이상이면 Over100ContentException.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        payload = {
            'title': 'post' * 26,
            'content': 'This is content',
        }
        res = self.client.post(POST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

