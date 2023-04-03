from django.contrib.auth import get_user_model
from rest_framework import filters, status, viewsets, mixins, serializers
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from api.permissions import OwnerOrReadOnly
from api.serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)
from posts.models import Follow, Group, Post

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrReadOnly,)

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get("post_id"))
        return post.comments.all()

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.kwargs.get("post_id"))
        serializer.save(post=post, author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (OwnerOrReadOnly,)


class CreateRetrieveViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    pass


class FollowCreateRetrieveViewSet(CreateRetrieveViewSet):
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("=following__username",)

    def get_queryset(self):
        return self.request.user.follow.all()

    # def create(self, request, *args, **kwargs):
    #     following = request.data.get("following")
    #     follow = self.request.user.follow.filter(following__username=following)
    #     if follow or self.request.user.username == following:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #     return super().create(request, *args, **kwargs)
    #
    # def perform_create(self, serializer):
    #     following = User.objects.get(
    #         username=self.request.data.get("following")
    #     )
    #     serializer.save(user=self.request.user, following=following)
