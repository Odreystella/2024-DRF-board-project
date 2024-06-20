from rest_framework import generics

from users.serializers import UserSerializer


class UserSignUpView(generics.CreateAPIView):
    """
    회원가입 컨트롤러.
    """
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return response
