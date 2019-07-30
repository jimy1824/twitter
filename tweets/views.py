from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from .serializers import TweetListSerializer
import requests
from bs4 import BeautifulSoup


class TweetsListView(APIView):
    serializers_class = TweetListSerializer
    twitter_url = 'https://twitter.com/'

    def get_profile_url(self, twitter_user_name):
        user_profile_url = self.twitter_url + twitter_user_name
        return requests.get(user_profile_url)

    def get_account_info(self, header, tweet_dict):
        profile = header.find('a', {
            'class': 'account-group js-account-group js-action-profile js-user-profile-link js-nav'})
        fullname = profile.find('strong', {'class': 'fullname show-popup-with-id u-textTruncate'}).text
        tweet_dict['account'] = {'id': profile.get('data-user-id'), 'full_name': fullname, 'href': profile.get('href')}
        return tweet_dict

    def get_hashtags(self, content, tweet_dict):
        hashtags = content.find_all('a', {'class': 'twitter-hashtag pretty-link js-nav'})
        hashtags_list = []
        for hashtag in hashtags:
            hashtags_list.append(hashtag.text)
        tweet_dict['hashtags'] = hashtags_list
        return tweet_dict

    def get_stat(self, content, tweet_dict):
        footer = content.find('div', {'class': 'stream-item-footer'})
        stat = footer.find('div', {'class': 'ProfileTweet-actionCountList u-hiddenVisually'}).text.replace("\n",
                                                                                                           " ").strip()
        replies_count, replies, retweets_count, retweets, likes_count, likes = stat.split()
        tweet_dict['replies'] = int("".join(replies_count.replace(',', '')))
        tweet_dict['retweets'] = int("".join(retweets_count.replace(',', '')))
        tweet_dict['likes'] = int("".join(likes_count.replace(',', '')))
        return tweet_dict

    def get_tweets_list(self, request_response, limit):
        list_of_tweets = []
        bs = BeautifulSoup(request_response.content, 'lxml')
        all_tweets = bs.find_all('div', {'class': 'tweet'})
        if all_tweets:
            for tweet in all_tweets[:limit]:
                tweet_dict = {}
                content = tweet.find('div', {'class': 'content'})
                header = content.find('div', {'class': 'stream-item-header'})
                tweet_dict = self.get_account_info(header, tweet_dict)
                tweet_dict = self.get_hashtags(content, tweet_dict)
                tweet_dict = self.get_stat(content, tweet_dict)
                tweet_dict['text'] = content.find('div', {'class': 'js-tweet-text-container'}).text.replace("\n",
                                                                                                            " ").strip()
                tweet_dict['date'] = header.find('a', {'class': 'tweet-timestamp js-permalink js-nav js-tooltip'}).get(
                    'title')
                list_of_tweets.append(tweet_dict)
        return list_of_tweets

    def get_tweets(self, twitter_user_name, limit):
        resquest_response = self.get_profile_url(twitter_user_name)
        if resquest_response.status_code == 200:
            return self.get_tweets_list(resquest_response, limit)

    def get(self, request, *args, **kwargs):
        twitter_user_name = kwargs.get('twitter_user_name')
        limit = request.GET.get('limit', 10)
        return Response(self.serializers_class(self.get_tweets(twitter_user_name, int(limit)), many=True).data,
                        status=HTTP_200_OK)
