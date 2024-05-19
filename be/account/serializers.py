from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    posts_count=serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'followers_count', 'following_count','posts_count')

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()