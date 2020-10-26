import tweepy as tw
import pandas as pd
from tqdm import tqdm, notebook
from pymongo import MongoClient
import json
import datetime


consumer_api_key = 'OSdFGWDBz2bhEHl2SNeQrUn8W'
consumer_api_secret = 'qVvrYEJtURWyUawdUQKZ81kbedp4VLhheGoU7wGjt1GSSCXoHr'

auth = tw.OAuthHandler(consumer_api_key, consumer_api_secret)
api = tw.API(auth, wait_on_rate_limit=True)

#设置搜索关键词
search_words = "#covid19 -filter:retweets"
date_since = "2020-03-01"
# Collect tweets
tweets = tw.Cursor(api.search,
              q=search_words,
              lang="en",
              since=date_since).items(10)#爬取推特数量

tweets_copy = []
for tweet in tqdm(tweets):
     tweets_copy.append(tweet)


# Auth Variables
consumer_key = 'OSdFGWDBz2bhEHl2SNeQrUn8W'
consumer_key_secret = 'qVvrYEJtURWyUawdUQKZ81kbedp4VLhheGoU7wGjt1GSSCXoHr'
access_token = "1320360870971502594-szc1KJoTaP16arW58RXibr3fu8YGGW"
access_token_secret = "8AOz4ynovteIWrWsRi8GgLP5fbAenxYzBxOlZ584bFlKx"


connection = MongoClient("mongodb://msbd5003-db-server.eastasia.cloudapp.azure.com:27017/")
db = connection['MSBD5003']
collection = db.tweets

for tweet in tqdm(tweets_copy):
    tweet_id = tweet.id_str  # The Tweet ID from Twitter in string format
    text = tweet.text  # The entire body of the Tweet
    hashtags = tweet.entities['hashtags']  # Any hashtags used in the Tweet
    created = tweet.created_at
    tweet_dic = {'id': tweet_id, 'text': text, 'hashtags': hashtags, 'created': created}
    collection.insert(tweet_dic)
    