"""
1. 회원가입 - 인증되지 않은 상태에서 요청할 수 있음
    - POST /api/v1/users/signup
    - 이메일, 이름, 비밀번호 받아 회원가입 성공 케이스
    - 이메일이 기존에 있는 경우 에러 케이스
    - 비밀번호가 8자 이상, 소문자, 대문자, 특수문자 각 1자리 이상 포함되지 않은 경우 실패 케이스
    - 이름이 없으면 유저 이메일 @앞부분 잘라서 디폴트값 생성 케이스

2. 로그인 - 인증되지 않은 상태에서 요청할 수 있음
    - POST /api/v1/users/signin
    - 이메일, 비밀번호 받아 인증되면 jwt 토큰과 유저정보 반환
    - 이메일이 존재하지 않으면 에러 케이스 UserNotFound
    - 인증에 실패할 경우 에러 케이스 PasswordNotMatched

3. jwt 토큰 발급 - 인증되지 않은 상태에서 요청할 수 있음
    - 이메일, 비밀번호 받아 인증되면 jwt 토큰 발급

4. 회원정보 수정/탈퇴시 비밀번호 인증 - 인증된 상태에서 요청할 수 있음
    - POST /api/v1/users/me
    - 비밀번호를 받아 인증에 성공하는 케이스
    - jwt 토큰이 없으면 401 에러
    - 비밀번호가 일치하지 않는 경우 에러 케이스 PasswordNotMatched

5. 회원정보 수정 - 인증된 상태에서 요청할 수 있음
    - PATCH /api/v1/users/me
    - jwt토큰으로 이름 및 비밀번호 수정 성공 케이스
    - 토큰이 만료된 경우 401 에러

6. 회원 탈퇴하기 - 인증된 상태에서 요청할 수 있음
    - DELETE /api/v1/users/me
    - jwt토큰으로 탈퇴 성공 케이스
    - jwt토큰의 유저와 수정하려는 유저가 다를 경우 에러 케이스 IsNotMe
"""

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import (
    APITestCase,
    APIClient,
)
from rest_framework_simplejwt.tokens import RefreshToken


SIGNUP_URL = reverse('users:signup')
SIGNIN_URL = reverse('users:signin')
ME_URL = reverse('users:me')


class PublicUserApiTests(APITestCase):
    """
    인증이 필요하지 않는 APIs 테스트.
    """

    def setUp(self):
        self.client = APIClient()

        get_user_model().objects.create_user(
            name='Test',
            email='test@example.com',
            password='Test1234!',
        )

    def test_signup_success(self):
        """
        이름, 이메일, 비밀번호 받아 회원가입 성공 케이스.
        """
        payload = {
            'name': 'Test2',
            'email': 'test2@example.com',
            'password': 'Test1234!',
        }
        res = self.client.post(SIGNUP_URL, payload)

        user = get_user_model().objects.get(email=payload['email'])

        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_email_exists_error(self):
        """
        이메일이 기존에 있는 경우 에러 케이스.
        """
        payload = {
            'name': 'Test2',
            'email': 'test@example.com',
            'password': 'Test1234!',
        }
        res = self.client.post(SIGNUP_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_invalid_error(self):
        """
        비밀번호가 8자 이상, 소문자, 대문자, 특수문자 각 1자리 이상 포함되지 않은 경우 실패 케이스.
        """
        payload = {
            'name': 'Test2',
            'email': 'test2@example.com',
            'password': 'Test1234',
        }
        res = self.client.post(SIGNUP_URL, payload)

        user_not_exists = get_user_model().objects.filter(email=payload['email']).exists()

        self.assertFalse(user_not_exists)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_username_setdefault_when_empty_input(self):
        """
        이름이 없으면 유저 이메일 @앞부분 잘라서 디폴트값 생성 케이스
        """
        payload = {
            'name': '',
            'email': 'test2@example.com',
            'password': 'Test1234!',
        }
        res = self.client.post(SIGNUP_URL, payload)

        user = get_user_model().objects.get(email=payload['email'])

        self.assertEqual(user.name, user.email.split('@')[0])
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_login_success(self):
        """
        이메일, 비밀번호 받아 인증되면 jwt 토큰과 유저정보 반환.
        """
        payload = {
            'email': 'test@example.com',
            'password': 'Test1234!',
        }

        res = self.client.post(SIGNIN_URL, payload)

        self.assertIn('token_pair', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_not_found_error(self):
        """
        이메일이 존재하지 않으면 에러 케이스 UserNotFound.
        """
        payload = {
            'email': 'test1@example.com',
            'password': 'Test1234!',
        }
        res = self.client.post(SIGNIN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('해당 이메일의 유저가 존재하지 않습니다.', res.data['detail'])

    def test_user_psssword_not_matched_error(self):
        """
        인증에 실패할 경우 에러 케이스 PasswordNotMatched.
        """
        payload = {
            'email': 'test@example.com',
            'password': 'Test1234@@',
        }

        res = self.client.post(SIGNIN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('인증에 실패하였습니다.', res.data['detail'])


class PrivateUserApiTests(APITestCase):
    """
    인증이 필요한 APIs 테스트.
    """
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            name='Test',
            email='test@example.com',
            password='Test1234!',
        )
        self.client = APIClient()

        refresh = RefreshToken.for_user(self.user)
        self._access_token = refresh.access_token
        self.access_token = str(refresh.access_token)

    def test_user_is_authenticated_with_password_success(self):
        """
        비밀번호를 받아 인증에 성공하는 케이스.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        payload = {
            'password': 'Test1234!',
        }
        res = self.client.post(ME_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_unauthorized_without_jwt_error(self):
        """
        jwt 토큰이 없으면 401 에러.
        """
        payload = {
            'password': 'Test1234!',
        }
        res = self.client.post(ME_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_is_not_authenticated_with_password_error(self):
        """
        비밀번호가 일치하지 않는 경우 에러 케이스 PasswordNotMatched.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        payload = {
            'password': 'Test1234!!!!',
        }
        res = self.client.post(ME_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('인증에 실패하였습니다.', res.data['detail'])

    def test_user_info_updated_success(self):
        """
        jwt토큰으로 이름 및 비밀번호 수정 성공 케이스
        """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        payload = {
            'name': '',
            'password': 'Test1234!!!!',
        }
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()

        self.assertTrue(self.user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_info_not_updated_with_invalid_jwt_error(self):
        """
        토큰이 만료된 경우 401 에러
        """
        self._access_token.set_exp(lifetime=timedelta(seconds=-1))

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self._access_token))
        payload = {
            'name': 'new_name',
            'password': ''
        }
        res = self.client.patch(ME_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


