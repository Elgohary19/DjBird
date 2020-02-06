from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from rest_framework import serializers
from ..models import UserProfile


User = get_user_model()


class UserDisplaySerializer(serializers.ModelSerializer):
    follower_count = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = (
            'username',
            'first_name',
            'last_name',
            'follower_count',
            'url',
            'get_avatar',
            #'email',
        )

    def get_follower_count(self, obj):
        return 0

    def get_url(self, obj):
        return reverse_lazy("profiles:detail", kwargs={"username": obj.username})
