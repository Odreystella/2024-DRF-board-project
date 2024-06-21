from rest_framework import serializers

from core.models import Post


class PostListSerializer(serializers.ModelSerializer):
    """
    목록 조회시, 제목, 사용자 이름, 조회수 보여주는 시리얼라이저.
    """

    creator = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'creator', 'view_count']

    def get_creator(self, obj):
        if obj.user.is_deleted:
            return '탈퇴한 유저'
        return obj.user.name


class PostSerializer(serializers.ModelSerializer):
    """
    게시글 생성/조회/수정/삭제시, 제목, 내용, 사용자 이름, 작성시간, 수정시간(수정되지 않았다면 빈값..) 보여주는 시리얼라이저.
    """

    creator = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'content',
            'creator',
            'created_at',
            'updated_at',
            'view_count',
            'is_deleted',
        ]

    def get_creator(self, obj):
        if obj.user.is_deleted:
            return '탈퇴한 유저'
        return obj.user.name
