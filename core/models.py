from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
)

from users.exceptions import EmailRequiredException


class Shared(models.Model):
    """
    공통으로 사용하는 모델.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    """
    커스텀 유저 매니저.
    """
    def create_user(self, email, password=None, **extra_field):
        """
        유저 생성 메서드.
        """
        if not email:
            raise EmailRequiredException

        user = self.model(email=self.normalize_email(email), **extra_field)
        user.set_password(password)
        user.save(using=self.db)
        return user


class User(AbstractBaseUser, Shared):
    """
    커스텀 유저 모델.
    """
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()
