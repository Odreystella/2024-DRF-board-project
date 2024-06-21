from django.urls import path

from users import views


app_name = 'users'

urlpatterns = [
    path('/signup', views.UserSignUpView.as_view(), name='signup'),
    path('/signin', views.UserSignInView.as_view(), name='signin'),
    path('/me', views.UserUpdateView.as_view(), name='me'),
]