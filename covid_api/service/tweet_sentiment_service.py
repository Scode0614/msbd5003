from repository.tweets import TweetsRepository
from repository.tweets import SENTIMENT_LABEL as TWEET_SENTIMENT_LABEL
from repository.tweets import META as TWEET_META

from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd

class TweetSentimentService:
  def __init__(self, collection_uri: str, spark):
    self.tweet_repo = TweetsRepository(collection_uri, spark)

  def info(self, from_date: str, to_date: str, keywords: list):
    tweet_df = self.get_tweets_by_dates(from_date, to_date, keywords)
    if len(tweet_df) == 0:
      return {}
    top_sentiment_words = self.get_top_sentiment_words(tweet_df, 100)
    sentiment_counts = self.get_sentiment_tweets_counts(tweet_df)
    sentiment_daily_counts = self.get_sentiment_tweets_daily_counts(tweet_df)
    top_sentiment_tweets = self.get_top_n_sentiment_tweets(tweet_df, 100)
    return {
      'top_sentiment_words': top_sentiment_words,
      'sentiment_counts': sentiment_counts,
      'sentiment_daily_counts': sentiment_daily_counts,
      'top_sentiment_tweets': top_sentiment_tweets
    }

  def get_tweets_by_dates(self, from_date: str, to_date: str, keywords: list):
    return self.tweet_repo.get_tweets_by_dates(from_date, to_date, keywords)

  def get_top_sentiment_words(self, tweet_df, size):
    # init count vector
    cvec = CountVectorizer()
    cvec.fit(tweet_df[TWEET_META.TEXT])

    # transform each label data to matrix
    pos_doc_matrix = cvec.transform(tweet_df[tweet_df[TWEET_META.LABEL]==TWEET_SENTIMENT_LABEL.POS][TWEET_META.TEXT_CLEANED])
    neg_doc_matrix = cvec.transform(tweet_df[tweet_df[TWEET_META.LABEL]==TWEET_SENTIMENT_LABEL.NEG][TWEET_META.TEXT_CLEANED])
    neu_doc_matrix = cvec.transform(tweet_df[tweet_df[TWEET_META.LABEL]==TWEET_SENTIMENT_LABEL.NEU][TWEET_META.TEXT_CLEANED])

    # count each label
    pos_tf = np.sum(pos_doc_matrix,axis=0)
    neg_tf = np.sum(neg_doc_matrix,axis=0)
    neu_tf = np.sum(neu_doc_matrix,axis=0)

    pos_words = np.squeeze(np.asarray(pos_tf))
    neg_words = np.squeeze(np.asarray(neg_tf))
    neu_words = np.squeeze(np.asarray(neu_tf))

    term_freq_df = pd.DataFrame([pos_words, neg_words, neu_words],columns=cvec.get_feature_names()).transpose()
    term_freq_df.columns = ['positive','negative','natural']
    term_freq_df['total'] = term_freq_df['negative'] + term_freq_df['positive'] + term_freq_df['natural']

    pos_words = term_freq_df.sort_values(by='positive', ascending=False)[['positive']].iloc[:size]
    neg_words = term_freq_df.sort_values(by='negative', ascending=False)[['negative']].iloc[:size]
    all_words = term_freq_df.sort_values(by='total', ascending=False)[['total']].iloc[:size]
    return {
      'pos': {"word":list(pos_words.index),"count":list(pos_words.positive)},
      'neg': {"word":list(neg_words.index),"count":list(neg_words.negative)},
      'total': {"word":list(all_words.index),"count":list(all_words.total)}
    }

    
  def get_sentiment_tweets_counts(self, tweet_df):
    return {
      'pos': len(tweet_df[tweet_df[TWEET_META.LABEL]==TWEET_SENTIMENT_LABEL.POS]),
      'neg': len(tweet_df[tweet_df[TWEET_META.LABEL]==TWEET_SENTIMENT_LABEL.NEG]),
      'neu': len(tweet_df[tweet_df[TWEET_META.LABEL]==TWEET_SENTIMENT_LABEL.NEU])
    }

  def get_sentiment_tweets_daily_counts(self, tweet_df):

    # pick pos/neg/neu list separately
    pos_df = tweet_df[tweet_df[TWEET_META.LABEL]==TWEET_SENTIMENT_LABEL.POS][[TWEET_META.DATE, TWEET_META.LABEL]]
    neg_df = tweet_df[tweet_df[TWEET_META.LABEL]==TWEET_SENTIMENT_LABEL.NEG][[TWEET_META.DATE, TWEET_META.LABEL]]
    neu_df = tweet_df[tweet_df[TWEET_META.LABEL]==TWEET_SENTIMENT_LABEL.NEU][[TWEET_META.DATE, TWEET_META.LABEL]]

    # format date with only yyyy-mm-dd
    pos_df['date'] = pos_df[TWEET_META.DATE].map(lambda x: x[0:10])
    neg_df['date'] = neg_df[TWEET_META.DATE].map(lambda x: x[0:10])
    neu_df['date'] = neu_df[TWEET_META.DATE].map(lambda x: x[0:10])

    # group by date, and convert to list of tuples (date, count)
    pos_df_daily_count = pos_df.groupby('date').count()[[TWEET_META.LABEL]]
    neg_df_daily_count = neg_df.groupby('date').count()[[TWEET_META.LABEL]]
    neu_df_daily_count = neu_df.groupby('date').count()[[TWEET_META.LABEL]]

    return {
      'pos': {"date":list(pos_df_daily_count.index),"count":list(pos_df_daily_count[TWEET_META.LABEL])},
      'neg': {"date":list(neg_df_daily_count.index),"count":list(neg_df_daily_count[TWEET_META.LABEL])},
      'neu': {"date":list(neu_df_daily_count.index),"count":list(neu_df_daily_count[TWEET_META.LABEL])}
    }

  def get_top_n_sentiment_tweets(self, tweet_df, size):
    df_pos = tweet_df.sort_values(by='compound', ascending=False).iloc[:size][[TWEET_META.TEXT, TWEET_META.DATE, TWEET_META.COMPOUND]]
    df_neg = tweet_df.sort_values(by='compound', ascending=True).iloc[:size][[TWEET_META.TEXT, TWEET_META.DATE, TWEET_META.COMPOUND]]
    return {
      'pos': {"date":list(df_pos[TWEET_META.DATE]),"text":list(df_pos[TWEET_META.TEXT]),"score":list(df_pos[TWEET_META.COMPOUND])},
      'neg': {"date":list(df_neg[TWEET_META.DATE]),"text":list(df_neg[TWEET_META.TEXT]),"score":list(df_neg[TWEET_META.COMPOUND])}
    }