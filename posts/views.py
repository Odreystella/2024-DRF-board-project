from django.contrib.auth import get_user_model

from rest_framework import generics, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication


from core.models import Post
from users.exceptions import EmptyInputException, UserNotFoundException, IsNotMeException
from posts.serializers import PostListSerializer, PostSerializer
from posts.exceptions import PostNotFoundException


class PostListCreateView(generics.GenericAPIView):
    """
    게시글 목록 조회 및 게시글 생성 컨트롤러.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Post.objects.filter(is_deleted=False) \
                            .select_related('user') \
                            .only('title', 'user__name', 'view_count') \
                            .order_by("-created_at")

    def get(self, request, *args, **kwargs):
        """
        토큰 없이 게시글 목록 가져오는 API

        :param limit: int
        :param offset: int
        :param ordering: str

        """
        limit = int(request.query_params.get("limit", 10))
        offset = int(request.query_params.get("offset", 0))

        queryset = self.get_queryset()[offset : offset + limit]
        serializer = self.get_serializer()
        serializer = serializer(queryset, many=True)
        data = {
            'count': queryset.count(),
            'results': serializer.data
        }
        return Response(data)

    def post(self, request, *args, **kwargs):
        """
        토큰과 데이터로 게시글 생성하는 API

        :param title: str
        :param content: str

        """
        title = request.data.get('title')
        content = request.data.get('content')
        if not title or not content:
            raise EmptyInputException

        serializer = self.get_serializer()
        serializer = serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permission() for permission in self.permission_classes]
        return [AllowAny()]

    def get_authenticators(self):
        if self.request.method == 'POST':
            return [auth() for auth in self.authentication_classes]
        return []

    def get_serializer(self):
        if self.request.method == 'POST':
            return PostSerializer
        return PostListSerializer


class PostRetrieveUpdateDestroyView(generics.GenericAPIView):
    """
    게시글 조회/수정/삭제 컨트롤러.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        """
        토큰 없이 게시글 디테일 가져오는 API
        """
        try:
            post = self.get_object()
        except Post.DoesNotExist:
            raise PostNotFoundException

        post.view_count += 1
        post.save(update_fields=['view_count'])

        serializer = self.get_serializer(post)

        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        """
        토큰으로 게시글 수정하는 API

        :param title: str
        :param content: str

        """
        title = request.data.get('title')
        content = request.data.get('content')

        try:
            post = self.get_object()
        except Post.DoesNotExist:
            raise PostNotFoundException

        try:
            user = get_user_model().objects.get(email=request.user.email)
        except get_user_model().DoesNotExist:
            raise UserNotFoundException

        if post.user.pk != request.user.pk:
            raise IsNotMeException

        if title:
            post.title = title
        if content:
            post.content = content
        post.save(update_fields=['title', 'content'])

        serializer = self.get_serializer(post)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """
        토큰으로 게시글 삭제하는 API
        """
        try:
            post = self.get_object()
        except Post.DoesNotExist:
            raise PostNotFoundException

        try:
            user = get_user_model().objects.get(email=request.user.email)
        except get_user_model().DoesNotExist:
            raise UserNotFoundException

        if post.user.pk != request.user.pk:
            raise IsNotMeException

        post.is_deleted = True
        post.save(update_fields=['is_deleted'])

        serializer = self.get_serializer(post)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [permission() for permission in self.permission_classes]
        return [AllowAny()]

    def get_authenticators(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [auth() for auth in self.authentication_classes]
        return []
