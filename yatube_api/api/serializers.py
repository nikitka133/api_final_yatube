from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        fields = "__all__"
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        fields = "__all__"
        model = Comment
        read_only_fields = ("post",)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugField(read_only=True)
    following = serializers.SlugField()

    def validate(self, attrs):
        request = self.context.get("request")
        user = request.user
        username = request.data.get('following')

        following = get_object_or_404(
            User.objects, username=username
        )

        if user == following:
            raise serializers.ValidationError(
                "You can't subscribe for yourself"
            )

        if user.follow.filter(following__username=username):
            raise serializers.ValidationError(
                "You have already subscribed to this author"
            )

        attrs["user"] = user
        attrs['following'] = following

        return attrs

    class Meta:
        fields = ("user", "following")
        model = Follow
