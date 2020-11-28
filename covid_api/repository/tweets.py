from enum import Enum
from pyspark.sql.functions import udf
from pyspark.sql.types import *
from datetime import date, timedelta, datetime
from datetime import datetime
import pandas as pd

cache = {}

class TweetsRepository:
  def __init__(self, collection_uri: str, spark):
    self.df = spark.read.format("mongo").option("uri", collection_uri).load()

  ################################################################################################
  # Get Tweets from DB within the given date range
  # Inputs:
  # 1) from_date: YYYY-MM-DD, e.g: 2020-01-01
  # 2) to_date: YYYY-MM-DD, e.g: 2020-01-01
  # Return:
  #   SparkSQL DataFrame
  #     cols: - id:                  original tweet id
  #           - text:                original tweet content
  #           - created:             tweet created date, YYYY-MM-DDThh:mm:ss
  #           - neg:                 negative sentiment score, float
  #           - neu:                 natural sentiment score, float
  #           - pos:                 positive sentiment score, float
  #           - text_cleaned:        cleaned text data
  #           - compound:            compound sentiment score, float
  #           - sentiment_label:     sentiment label, -1 neg, 0 natural, 1 pos
  ################################################################################################
  def get_tweets_by_dates(self, from_date, to_date, keywords):
    end = datetime.strptime(to_date, "%Y-%m-%d")
    start = datetime.strptime(from_date, "%Y-%m-%d")
    date_range = pd.date_range(start, end - timedelta(days=1),freq='d')
    date_str_range = list(date_range.map(lambda x: str(x)[:10]))

    df = None
    for date in date_str_range:
      df1 = self.get_from_cache(date)
      if df == None:
        df = df1
      else:
        df = df.unionAll(df1)
      print(df.count())
      
    def intersect(row):
      # convert each word in lowecase
      row = [x.lower() for x in row.split()]
      return True if set(row).intersection(set(keywords)) else False

    if len(keywords) > 0:
      filterUDF = udf(intersect, BooleanType())
      df = df.where(filterUDF(df.text))
    return df.toPandas()
  
  def get_from_cache(self, date):
    if date not in cache.keys():
      if len(cache) >= 100:
        cache.pop(list(cache.keys())[0])
      df = self.df.where("created <= '" + date + " 23:59' and created >= '" + date + " 00:00'") \
      .select('id', 'text', 'created', 'neg', 'neu', 'pos', 'text_cleaned', 'compound', 'label')
      cache[date] = df
    return cache[date] 


class SENTIMENT_LABEL(int):
  POS = 1
  NEG = -1
  NEU = 0


class META(str):
  POS = 'pos'
  NEG = 'neg'
  NEU = 'neu'
  TEXT = 'text'
  TEXT_CLEANED = 'text_cleaned'
  COMPOUND = 'compound'
  LABEL = 'label'
  DATE = 'created'
  ID = 'id'