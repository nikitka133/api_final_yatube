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

    def create(self, validated_data):
        user = self.context.get('request').user
        following = get_object_or_404(
            User.objects, username=validated_data['following']
        )

        if user == following:
            raise serializers.ValidationError(
                            "You can't subscribe for yourself"
)
        validated_data['user'] = user
        validated_data['following'] = following
        obj, created = Follow.objects.get_or_create(**validated_data)

        if not created:
            raise serializers.ValidationError(
                "You have already subscribed to this author"
            )

        return obj

    class Meta:
        fields = ("user", "following")
        model = Follow
