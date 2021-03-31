from rest_framework.viewsets import ModelViewSet, ViewSetMixin
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import filters, generics
from django_filters.rest_framework import DjangoFilterBackend

from .models import Comment, Group, Post, Follow
from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer, GroupSerializer, PostSerializer,
                          FollowSerializer)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group']

    def perform_create(self, serializer):
        """ Переопределяем функцию, сохраняем поле автора"""
        return serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]

    def get_queryset(self, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id',))
        return post.comments.all()

    def perform_create(self, serializer, **kwargs):
        """ Переопределяем функцию, сохраняем поле автора"""
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post_id=post.id)


class GroupViewSet(ViewSetMixin, generics.ListCreateAPIView):
    """Использую миксины чтобы ограничить класс"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]


class FollowViewSet(ViewSetMixin, generics.ListCreateAPIView):
    """Использую миксины чтобы ограничить класс"""
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__username', '=author__username']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
