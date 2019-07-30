from rest_framework import serializers

class AccountSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=200)
    href = serializers.CharField(max_length=200)
    id = serializers.CharField(max_length=200)

class HashtagsSerializer(serializers.Serializer):
    hashtag= serializers.CharField(max_length=200)

class TweetListSerializer(serializers.Serializer):
    account=AccountSerializer()
    date = serializers.CharField(max_length=200)
    hashtags =serializers.SerializerMethodField()
    replies = serializers.IntegerField()
    retweets = serializers.IntegerField()
    likes = serializers.IntegerField()
    text = serializers.CharField()
    def get_hashtags(self, obj):
        print(obj.get("hashtags"))
        return HashtagsSerializer(obj.get("hashtags"), many=True).data

