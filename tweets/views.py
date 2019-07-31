from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from .serializers import TweetListSerializer
from bs4 import BeautifulSoup
from twitter import services
from twitter.constant import TWEETS_URL, DEFAULT_LIMIT, MAX_LIMIT, INVALID_URL_ERROR, TWEET_CLASS, LIMIT_OUTOF_BOUND


class TweetsListView(APIView):
    serializers_class = TweetListSerializer

    def get_tweets_list(self, page_source, limit):
        list_of_tweets = []
        bs = BeautifulSoup(page_source, 'lxml')
        all_tweets = bs.find_all('div', {'class': 'tweet'})
        if all_tweets:
            for tweet in all_tweets[:limit]:
                tweet_dict = {}
                content = tweet.find('div', {'class': 'content'})
                header = content.find('div', attrs={'class': 'stream-item-header'})
                tweet_dict = services.get_stat(tweet, services.get_hashtags(tweet, services.get_account_info(header,
                                                                                                             tweet_dict)))
                tweet_dict['text'] = tweet.find('div', {'class': 'js-tweet-text-container'}).text.replace("\n",
                                                                                                          " ").strip()
                tweet_dict['date'] = header.find('a', {'class': 'tweet-timestamp js-permalink js-nav js-tooltip'}).get(
                    'title')
                list_of_tweets.append(tweet_dict)
        return list_of_tweets

    def get_tweets(self, twitter_user_name, limit):
        url = TWEETS_URL.format(twitter_user_name)
        resquest_response = services.url_validation(url, TWEET_CLASS)
        if resquest_response:
            page_source = services.get_page_content(url, limit, TWEET_CLASS)
            return self.get_tweets_list(page_source, limit)
        return None

    def get(self, request, *args, **kwargs):
        twitter_user_name = kwargs.get('twitter_user_name')
        limit = int(request.GET.get('limit', DEFAULT_LIMIT))
        if (limit > MAX_LIMIT) or (limit < 0):
            return Response({'error': LIMIT_OUTOF_BOUND}, status=HTTP_400_BAD_REQUEST)
        tweets = self.get_tweets(twitter_user_name, limit)
        return Response(self.serializers_class(tweets, many=True).data, status=HTTP_200_OK) if tweets else Response(
            {'error': INVALID_URL_ERROR},
            status=HTTP_204_NO_CONTENT)
