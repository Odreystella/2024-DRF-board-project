from django.urls import path

from posts import views


app_name = 'posts'

urlpatterns = [
    path('', views.PostListCreateView.as_view(), name='list_and_create'),
    path('/<int:pk>', views.PostRetrieveUpdateDestroyView.as_view(), name='detail'),
]