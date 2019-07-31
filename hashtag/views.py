from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from tweets.serializers import TweetListSerializer
from twitter import services
from bs4 import BeautifulSoup
from twitter.constant import HASHTAG_URL, DEFAULT_LIMIT, INVALID_URL_ERROR, HASHTAG_TWEET_CLASS, MAX_LIMIT, \
    LIMIT_OUTOF_BOUND


class HashTagsListView(APIView):
    serializers_class = TweetListSerializer

    def get_tweets_list(self, page_source, limit):
        list_of_tweets = []
        bs = BeautifulSoup(page_source, 'lxml')
        all_tweets = bs.find_all('div', attrs={'class': 'content'})
        if all_tweets:
            for tweet in all_tweets[:limit]:
                tweet_dict = {}
                header = tweet.find('div', attrs={'class': 'stream-item-header'})
                tweet_dict = services.get_stat(tweet, services.get_hashtags(tweet, services.get_account_info(header,
                                                                                                             tweet_dict)))
                tweet_dict['text'] = tweet.find('div', {'class': 'js-tweet-text-container'}).text.replace("\n",
                                                                                                          " ").strip()
                tweet_dict['date'] = header.find('a', {'class': 'tweet-timestamp js-permalink js-nav js-tooltip'}).get(
                    'title')
                list_of_tweets.append(tweet_dict)
        return list_of_tweets

    def get_tweets(self, hashtag, limit):
        url = HASHTAG_URL.format(hashtag)
        resquest_response = services.url_validation(url, HASHTAG_TWEET_CLASS)
        if resquest_response:
            page_source = services.get_page_content(url, limit, HASHTAG_TWEET_CLASS)
            return self.get_tweets_list(page_source, limit)
        return None

    def get(self, request, *args, **kwargs):
        hashtag = kwargs.get('hashtag')
        limit = int(request.GET.get('limit', DEFAULT_LIMIT))
        if (limit > MAX_LIMIT) or (limit < 0):
            return Response({'error': LIMIT_OUTOF_BOUND}, status=HTTP_400_BAD_REQUEST)
        tweets = self.get_tweets(hashtag, limit)
        return Response(self.serializers_class(tweets, many=True).data, status=HTTP_200_OK) if tweets else Response(
            {'ValidationError': INVALID_URL_ERROR},
            status=HTTP_204_NO_CONTENT)
