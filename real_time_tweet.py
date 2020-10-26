from pymongo import MongoClient
import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import datetime
import tweepy

# Auth Variables

consumer_key = 'OSdFGWDBz2bhEHl2SNeQrUn8W'
consumer_key_secret = 'qVvrYEJtURWyUawdUQKZ81kbedp4VLhheGoU7wGjt1GSSCXoHr'
access_token = "1320360870971502594-szc1KJoTaP16arW58RXibr3fu8YGGW"
access_token_secret = "8AOz4ynovteIWrWsRi8GgLP5fbAenxYzBxOlZ584bFlKx"

# MongoDB connection info
# uri = "mongodb://{username}:{password}@{host}:{port}/{db_name}?authMechanism=MONGODB-CR".format(username='hkust',
#                                                                        password='hkust',
#                                                                        host='msbd5003-db-server.eastasia.cloudapp.azure.com',
#                                                                        port=27017,
#                                                                        db_name='MSBD5003')
connection = MongoClient("mongodb://msbd5003-db-server.eastasia.cloudapp.azure.com:27017/")
db = connection['MSBD5003']
# db.authenticate('hkust','hkust')
db.tweets.ensure_index("id", unique=True, dropDups=True)
collection = db.tweets

# Key words to be tracked, (hashtags)

keyword_list = ['#covid-19']


class StdOutListener(StreamListener):
    def on_data(self, data):

        # Load the Tweet into the variable "t"
        t = json.loads(data)

        # Pull important data from the tweet to store in the database.
        tweet_id = t['id_str']  # The Tweet ID from Twitter in string format
        text = t['text']  # The entire body of the Tweet
        hashtags = t['entities']['hashtags']  # Any hashtags used in the Tweet
        timestamp = t['created_at']  # The timestamp of when the Tweet was created
        created = datetime.datetime.strptime(timestamp, '%a %b %d %H:%M:%S +0000 %Y')
        
        # Load all of the extracted Tweet data into the variable "tweet" that will be stored into the database
        tweet = {'id': tweet_id, 'text': text, 'hashtags': hashtags, 'created': created}

        # Save the refined Tweet data to MongoDB
        collection.insert(tweet)

        print(tweet_id + "\n")
        return True

    # Prints the reason for an error to your console
    def on_error(self, status):
        print(status)

l = StdOutListener(api=tweepy.API(wait_on_rate_limit=True))
auth = OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)

stream = Stream(auth, listener=l)
stream.filter(track=keyword_list,languages=["en"])