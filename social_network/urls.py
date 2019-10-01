from django.urls import path
from .views import *

app_name = 'social_network'
urlpatterns = [
    path('user/sign-up/', UserSignUp.as_view(), name='sign-up'),
    path('user/login/', UserLogin.as_view(), name='login'),
    path('user/logout/', UserLogout.as_view(), name='logout'),
    path('post/create/', PostCreateView.as_view(), name='post-create'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('post/interactive/<int:pk>/<str:type>/', PostLikeUnLikeView.as_view(), name='post-interactive'),
    path('post/detail/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
]
