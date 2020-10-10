import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
# predict the sentiment of Tweet, see 'https://textblob.readthedocs.io/en/dev/'
from textblob import TextBlob
# pip install Elasticsearch if not intalled yet
from elasticsearch import Elasticsearch
from datetime import datetime
import calendar
import numpy as np
from http.client import IncompleteRead

# log in to your Twitter Application Management to create an App, url: 'https://apps.twitter.com'
consumer_key = "wpjfstyikV9KrXhfmiVZfEc4y"
consumer_secret = "D9nPYlE3u8piuGeToToUU61m3IpMiKPhGZUmvziHJsPHs5Qrjo"
access_token = "1085687624004718592-OFt18RwTk2Fjs8iIkxNQJ7hGCTRc8k"
access_token_secret = "aJbXM453ABM6XYjZdadkDbSVfTuW8W4UlSnyheevlZAIY"

# create instance of elasticsearch
es = Elasticsearch()


class TweetStreamListener(StreamListener):

    # re-write the on_data function in the TweetStreamListener
    # This function enables more functions than 'on_status', see 'https://stackoverflow.com/questions/31054656/what-is-the-difference-between-on-data-and-on-status-in-the-tweepy-library'
    def on_data(self, data):
        # To understand the key-values pulled from Twitter, see 'https://dev.twitter.com/overview/api/tweets'
        dict_data = json.loads(data)
        # pass Tweet into TextBlob to predict the sentiment
        tweet = TextBlob(dict_data["text"]) if "text" in dict_data.keys() else None

        # if the object contains Tweet
        if tweet:
            # determine if sentiment is positive, negative, or neutral
            if tweet.sentiment.polarity < 0:
                sentiment = "negative"
            elif tweet.sentiment.polarity == 0:
                sentiment = "neutral"
            else:
                sentiment = "positive"

            # print the predicted sentiment with the Tweets
            print(sentiment, tweet.sentiment.polarity, dict_data["text"])

            # extract the first hashtag from the object
            # transform the Hashtags into proper case
            if len(dict_data["entities"]["hashtags"]) > 0:
                hashtags = dict_data["entities"]["hashtags"][0]["text"].title()
            else:
                # Elasticeach does not take None object
                hashtags = "None"

            # add text and sentiment info to elasticsearch
            es.index(index="test-tweet",
                     # create/inject data into the cluster with index as 'test-tweet'
                     # create the naming pattern in Management/Kibana later in order to push the data to a dashboard
                     doc_type="test-type",
                     body={"author": dict_data["user"]["screen_name"],
                           "followers": dict_data["user"]["followers_count"],
                           # parse the milliscond since epoch to elasticsearch and reformat into datatime stamp in Kibana later
                           "date": datetime.strptime(dict_data["created_at"], '%a %b %d %H:%M:%S %z %Y'),
                           "message": dict_data["text"] if "text" in dict_data.keys() else " ",
                           "hashtags": hashtags,
                           "polarity": tweet.sentiment.polarity,
                           "subjectivity": tweet.sentiment.subjectivity,
                           "sentiment": sentiment})
        return True

    # on failure, print the error code and do not disconnect
    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    # create instance of the tweepy tweet stream listener
    listener = TweetStreamListener()
    # set twitter keys/tokens
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # The most exception break up the kernel in my test is ImcompleteRead. This exception handler ensures
    # the stream to resume when breaking up by ImcompleteRead
    while True:
        try:
            # create instance of the tweepy stream
            stream = Stream(auth, listener)
            # search twitter for keyword "singapore"
            stream.filter(track=['singapore'])
        except IncompleteRead:
            continue
        except KeyboardInterrupt:
            # or however you want to exit this loop
            stream.disconnect()
            break