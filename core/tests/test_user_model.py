"""
테스트 케이스:
1. 유저 모델과 매니저의 내부 동작 성공 테스트.
2. 유저 이메일 표준화하는 성공 테스트.
3. 유저 이메일 빈값일 때, EmailRequiredException 발생 에러 테스트.
"""


from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase

from users.exceptions import EmailRequiredException


class UserModelTests(APITestCase):
    def test_create_user_with_email_success(self):
        """
        유저 모델과 매니저의 내부 동작 성공 테스트.
        """
        email = 'test@example.com'
        password = 'Test1234!'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_email_normalized_success(self):
        """
        유저 이메일 표준화하는 성공 테스트.
        """
        sample_emails = [
            ['Test1@ExAmple.com', 'Test1@example.com'],
            ['test2@Example.com', 'test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, normalized in sample_emails:
            user = get_user_model().objects.create_user(email, 'Test1234!')
            self.assertEqual(user.email, normalized)

    def test_user_without_email_error(self):
        """
        유저 이메일 빈값일 때, EmailRequiredException 발생 에러 테스트.
        """
        with self.assertRaises(EmailRequiredException):
            get_user_model().objects.create_user('', 'Test1234!')
