from django.contrib.auth import get_user_model

from rest_framework import serializers

from users.validators import validate_password


class UserSerializer(serializers.ModelSerializer):
    """
    유저 시리얼라이저.
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = get_user_model()
        fields = ['name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        """
        유효성 검사 통과 후, 유저가 생성되는 메서드.
        """
        return get_user_model().objects.create_user(**validated_data)
    
    def to_internal_value(self, data):
        try:
            data['name'] = data.get('email').split('@')[0]
        except AttributeError:
            _mutable = data._mutable
            data._mutable = True
            data['name'] = data.get('email').split('@')[0]
            data._mutable = _mutable
        return super().to_internal_value(data)