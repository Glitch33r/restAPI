from django.urls import path
from .views import *

app_name = 'social_network'
urlpatterns = [
    path('user/sign-up/', UserSignUp.as_view()),
    path('user/login/', UserLogin.as_view()),
    path('user/logout/', UserLogout.as_view()),
    path('post/create/', PostCreateView.as_view()),
    path('posts/', PostListView.as_view()),
    path('post/interactive/<int:pk>/<str:type>/', PostLikeUnLikeView.as_view()),
    path('post/detail/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
]
