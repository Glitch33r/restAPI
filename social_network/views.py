from rest_framework import generics
from .serializers import *
from .models import Post


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostDetailSerializer


class PostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostDetailSerializer
    queryset = Post.objects.all()


class PostLikeUnLikeView(generics.UpdateAPIView):
    serializer_class = PostLikeUnLikeSerializer
    queryset = Post.objects.all()

    def patch(self, request, *args, **kwargs):
        obj = self.get_object()
        if kwargs.get('type') == 'like':
            obj.likes += 1
        else:
            if obj.likes != 0:
                obj.likes -= 1
            else:
                obj.likes = 0

        obj.save()

        return self.partial_update(request, *args, **kwargs)
