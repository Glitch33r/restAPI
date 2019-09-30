from django.urls import path
from .views import *

app_name = 'social_network'
urlpatterns = [
    path('post/create/', PostCreateView.as_view()),
    path('posts/', PostListView.as_view()),
    path('post/interactive/<int:pk>/<str:type>', PostLikeUnLikeView.as_view()),
    path('post/detail/<int:pk>/', PostDetailView.as_view()),
]
