from rest_framework import serializers

class AccountSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=200)
    href = serializers.CharField(max_length=200)
    id = serializers.CharField(max_length=200)

class HashtagsSerializer(serializers.Serializer):
    hashtags= serializers.CharField(max_length=200)

class TweetListSerializer(serializers.Serializer):
    account=AccountSerializer()
    date = serializers.CharField(max_length=200)
    hashtags = serializers.CharField(max_length=200)
    replies = serializers.IntegerField()
    retweets = serializers.IntegerField()
    likes = serializers.IntegerField()
    text = serializers.CharField()

