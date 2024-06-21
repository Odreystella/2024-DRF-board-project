from django.contrib.auth import get_user_model, authenticate

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.serializers import (
    UserSerializer,
    UserTokenObtainPairSerializer,
    UserSignInSerializer
)
from users.exceptions import (
    EmptyInputException,
    TemporaryRedirectException,
    UserNotFoundException,
    PasswordNotMatchedException,
    IsNotMeException
)
from users.validators import validate_password


class UserSignUpView(generics.CreateAPIView):
    """
    회원가입 컨트롤러.
    """
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        """
        이름, 비밀번호, 이메일로 유저 생성하는 API

        :param name: str
        :param password: str
        :param email: str

        """
        response = super().create(request, *args, **kwargs)
        return response


class UserSignInView(generics.GenericAPIView):
    """
    로그인 컨트롤러.
    """
    serializer_class = UserTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """
        이메일, 비밀번호로 인증하는 API

        :param email: str
        :param password: str

        """
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            raise EmptyInputException

        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            raise UserNotFoundException

        if user.is_deleted:
            raise TemporaryRedirectException

        token_serializer = self.get_serializer(data=request.data)
        token_serializer.is_valid(raise_exception=True)

        user_serializer = UserSignInSerializer(user, context={'tokens': token_serializer.validated_data})
        return Response(user_serializer.data, status=status.HTTP_200_OK)


class UserUpdateView(generics.GenericAPIView):
    """
    유저 인증 후, 정보 수정 / 탈퇴 컨트롤러.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        """
        jwt 토큰과 비밀번호로 인증하는 API

        :param password: str

        """
        password = request.data.get('password')
        if not password:
            raise EmptyInputException

        user = authenticate(email=request.user.email, password=password)
        if user is None:
            raise PasswordNotMatchedException

        return Response({"detail": "유저 인증 성공."})

    def patch(self, request, *args, **kwargs):
        """
        이름 또는 비밀번호 수정하는 API

        :param name: str
        :param password: str

        """
        name = request.data.get('name')
        password = request.data.get('password')

        try:
            user = get_user_model().objects.get(email=request.user.email)
        except get_user_model().DoesNotExist:
            raise UserNotFoundException

        if user.id != request.user.id:
            raise IsNotMeException

        if name:
            user.name = name
        if password:
            valid_pw = validate_password(password)
            user.set_password(valid_pw)

        user.save(update_fields=['name', 'password'])

        return Response(self.get_serializer(user).data)

    def delete(self, request, *args, **kwargs):
        pass