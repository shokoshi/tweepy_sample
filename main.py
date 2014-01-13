#coding:utf-8

import tweepy
import sys
from keys import *

class MyStreamListener(tweepy.StreamListener):
    def __init__(self):
        self.count = 0
    
    def on_data(self, data):
        self.count += 1
        new_line = unicode(data, 'unicode_escape').encode('utf-8')
        new_line = new_line.replace('\\', '')
        print '---%3d---' % (self.count)
        print new_line
        if self.count == 10:
            sys.exit(0)
        return True

    def on_error(self, status):
        print status

def authorize(consumer_key, consumer_secret, access_token, access_secret):
    """ Authorize using OAuth.
    """
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return auth

def search_rest(auth, keyword, search_count=100):
    api = tweepy.API(auth_handler=auth)
    search_result = api.search(keyword, count=search_count)
    for i, twt in enumerate(search_result):
        print '---%3d---' % (i + 1)
        print twt.created_at
        print twt.user.name
        print twt.text + '\n'

def search_stream(auth, keyword):
    stream = tweepy.Stream(auth, MyStreamListener())
    stream.filter(track=[keyword])

def main():
    auth = authorize(KEYS['consumer_key'], KEYS['consumer_secret'],
            KEYS['access_token'], KEYS['access_secret'])

    if sys.argv[1] == 'rest':
        search_rest(auth, '中野', 100)
    elif sys.argv[1] == 'streaming':
        search_stream(auth, u'中野')
    else:
        print 'python %s [rest or streaming]' % sys.argv[0]

if __name__ == '__main__':
    main()
