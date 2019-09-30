from .serializers import *
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, status, permissions
from django.contrib.auth import authenticate, login, logout


class PostCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostDetailSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
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


class UserSignUp(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            refresh = RefreshToken.for_user(User.objects.filter(username=serializer.data.get('username')).first())
            token = {
                'User': 'Successfully created',
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
            }
            return Response(token, status=status.HTTP_201_CREATED)


class UserLogin(generics.GenericAPIView):

    def post(self, request):
        data = request.data

        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return Response({'Successfully logged!'}, status=status.HTTP_200_OK)
            else:
                return Response({'User is not active!'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'User is not found!'}, status=status.HTTP_404_NOT_FOUND)


class UserLogout(generics.GenericAPIView):
    def get(self, request):
        logout(request)
        return Response({'Successfully logged out!'}, status=status.HTTP_200_OK)
