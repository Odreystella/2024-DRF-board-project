from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.validators import validate_password
from users.exceptions import PasswordNotMatchedException


class UserSerializer(serializers.ModelSerializer):
    """
    유저 시리얼라이저.
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = get_user_model()
        fields = ['name', 'email', 'password', 'created_at', 'updated_at', 'is_deleted']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        """
        유효성 검사 통과 후, 유저가 생성되는 메서드.
        """
        return get_user_model().objects.create_user(**validated_data)
    
    def to_internal_value(self, data):
        if not data['name']:
            try:
                data['name'] = data.get('email').split('@')[0]
            except AttributeError:
                _mutable = data._mutable
                data._mutable = True
                data['name'] = data.get('email').split('@')[0]
                data._mutable = _mutable
        return super().to_internal_value(data)
    

class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    access_token, refresh_token 생성 시리얼라이저.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        self.user = authenticate(**data)

        if self.user is None:
            raise PasswordNotMatchedException

        data = {}
        refresh = self.get_token(self.user)

        data["access_token"] = str(refresh.access_token)
        data["refresh_token"] = str(refresh)

        return data


class UserSignInSerializer(serializers.Serializer):
    user = UserSerializer(source='*')
    token_pair = serializers.SerializerMethodField()

    def get_token_pair(self, obj):
        return self.context.get('tokens')