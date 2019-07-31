import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from .constant import BROWSER_HEADERS, PAGE_SCROLL_SCRIPT


def url_validation(url):
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': BROWSER_HEADERS, })
    return requests.get(url, headers=headers)


def check_limit(browser, limit,tweet_class):
    source_data = browser.page_source
    bs = BeautifulSoup(source_data, 'lxml')
    all_tweets = bs.find_all('div', attrs={'class': tweet_class})
    if len(all_tweets) >= limit:
        return True
    return False


def get_page_content(url, limit,tweet_class):
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(url)
    required_limit = False
    while not required_limit:
        len_of_page = browser.execute_script(PAGE_SCROLL_SCRIPT)
        if check_limit(browser, limit,tweet_class):
            required_limit = True
        browser.implicitly_wait(2)

    return browser.page_source


def get_account_info(header, tweet_dict):
    profile = header.find('a', {
        'class': 'account-group js-account-group js-action-profile js-user-profile-link js-nav'})
    fullname = profile.find('strong', {'class': 'fullname show-popup-with-id u-textTruncate'}).text
    tweet_dict['account'] = {'id': profile.get('data-user-id'), 'full_name': fullname, 'href': profile.get('href')}
    return tweet_dict


def get_hashtags(content, tweet_dict):
    hashtags = content.find_all('a', {'class': 'twitter-hashtag pretty-link js-nav'})
    hashtags_list = []
    for hashtag in hashtags:
        hashtag_dict = {'hashtag': hashtag.text}
        hashtags_list.append(hashtag_dict)
    tweet_dict['hashtags'] = hashtags_list
    return tweet_dict


def get_stat(content, tweet_dict):
    footer = content.find('div', {'class': 'stream-item-footer'})
    stat = footer.find('div', {'class': 'ProfileTweet-actionCountList u-hiddenVisually'}).text.replace("\n",
                                                                                                       " ").strip()
    replies_count, replies, retweets_count, retweets, likes_count, likes = stat.split()
    tweet_dict['replies'] = int("".join(replies_count.replace(',', '')))
    tweet_dict['retweets'] = int("".join(retweets_count.replace(',', '')))
    tweet_dict['likes'] = int("".join(likes_count.replace(',', '')))
    return tweet_dict
