from django.utils.timesince import timesince
from rest_framework import serializers

from accounts.api.serializers import UserDisplaySerializer


from tweets.models import Tweet


class ParentTweetModelSerializer(serializers.ModelSerializer):
    user = UserDisplaySerializer(read_only=True)
    date_display = serializers.SerializerMethodField()
    timesince = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    did_like = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()
    did_dislike = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = [
            'id',
            'user',
            'content',
            'timestamp',
            'date_display',
            'timesince',
            'likes',
            'dislikes',
            'did_like',
            'did_dislike',
        ]

    def get_did_like(self, object):
        request = self.context.get("request")
        try:
            user = request.user
            if user.is_authenticated:
                if user in object.liked.all():
                    return True
        except:
            pass
        return False

    def get_likes(self, object):
        return object.liked.all().count()

    def get_did_dislike(self, object):
        request = self.context.get("request")
        try:
            user = request.user
            if user.is_authenticated:
                if user in object.disliked.all():
                    return True
        except:
            pass
        return False

    def get_dislikes(self, object):
        return object.disliked.all().count()

    def get_date_display(self, obj):
        return obj.timestamp.strftime("%b %d, %Y | at %I %M %p")

    def get_timesince(self, obj):
        return timesince(obj.timestamp) + " ago"


class TweetModelSerializer(serializers.ModelSerializer):
    parent_id = serializers.CharField(write_only=True, required=False)
    user = UserDisplaySerializer(read_only=True)
    date_display = serializers.SerializerMethodField()
    timesince = serializers.SerializerMethodField()
    parent = ParentTweetModelSerializer(read_only=True)
    likes = serializers.SerializerMethodField()
    did_like = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()
    did_dislike = serializers.SerializerMethodField()


    class Meta:
        model = Tweet
        fields = [
            'parent_id',
            'id',
            'user',
            'content',
            'timestamp',
            'date_display',
            'timesince',
            'parent',
            'likes',
            'dislikes',
            'did_like',
            'did_dislike',
            'replay',
        ]

        #read_only_fields = ['replay']

    def get_did_like(self, object):
        request = self.context.get("request")
        try:
            user = request.user
            if user.is_authenticated:
                if user in object.liked.all():
                    return True
        except:
            pass
        return False

    def get_likes(self, object):
        return object.liked.all().count()

    def get_did_dislike(self, object):
        request = self.context.get("request")
        try:
            user = request.user
            if user.is_authenticated:
                if user in object.disliked.all():
                    return True
        except:
            pass
        return False

    def get_dislikes(self, object):
        return object.disliked.all().count()
    def get_date_display(self, obj):
        return obj.timestamp.strftime("%b %d, %Y | at %I %M %p")

    def get_timesince(self,obj):
        return timesince(obj.timestamp) + " ago"