from repository.tweets import TweetsRepository
from repository.tweets import SENTIMENT_LABEL as TWEET_SENTIMENT_LABEL
from repository.tweets import META as TWEET_META

from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from gensim import corpora, models

class HotTopicService:
  def __init__(self, collection_uri: str, spark):
    self.tweet_repo = TweetsRepository(collection_uri, spark)

  def info(self, from_date: str, to_date: str, keywords: list, similar_sentence: str):
    tweet_df = self.get_tweets_by_dates(from_date, to_date, keywords)
    if len(tweet_df) == 0:
      return {}
    top_words = self.get_top_words(tweet_df, 100)
    similar_tweets = self.get_similar_tweets(tweet_df, similar_sentence, 10)
    topic_keywords, topic_distribution, topic_counts = self.get_topic_info(tweet_df, 10)
    # top_sentiment_tweets = self.get_top_n_sentiment_tweets(tweet_df, 100)
    return {
      'top_words': top_words,
      'similar_tweets': similar_tweets,
      'topic_keywords': topic_keywords,
      'topic_distribution': topic_distribution,
      'topic_counts': topic_counts
    }

  def get_tweets_by_dates(self, from_date: str, to_date: str, keywords: list):
    return self.tweet_repo.get_tweets_by_dates(from_date, to_date, keywords)

  def get_top_words(self, tweet_df, size):
    # init count vector
    cvec = CountVectorizer(ngram_range=(2, 2), analyzer='word')
    cvec.fit(tweet_df[TWEET_META.TEXT])

    # transform each label data to matrix
    df_doc_matrix = cvec.transform(tweet_df[TWEET_META.TEXT_CLEANED])

    # count each labelcvec = CountVectorizer()
    df_tf = np.sum(df_doc_matrix,axis=0)
    df_words = np.squeeze(np.asarray(df_tf))
    term_freq_df = pd.DataFrame([df_words],columns=cvec.get_feature_names()).transpose()
    term_freq_df.columns = ['total']
    words = term_freq_df.sort_values(by='total', ascending=False)[['total']].iloc[:size]
    
    return {"word":list(words.index),"count":list(words.total)}

    
  def get_similar_tweets(self, tweet_df, sentence, size):
    keyword = sentence
    full_list = list(tweet_df[TWEET_META.TEXT_CLEANED])
    full_list.insert(0, keyword)

    v = TfidfVectorizer()
    v.fit(full_list)
    x = v.fit_transform(full_list)
    similarity_matrix = cosine_similarity(x)
    df_simiar_doc = pd.DataFrame(data={'text': full_list[1:], 'score': similarity_matrix[0][1:]})
    result = df_simiar_doc.sort_values(by=['score'], ascending=False).head(size)
    return {"text":list(result.text),"score":list(result.score)}

  def get_topic_info(self, tweet_df, size):
    cvec = CountVectorizer(ngram_range=(2, 3), analyzer='word')
    def twogram(text):
        try:
            cvec.fit([text])
            return cvec.get_feature_names()
        except:
            return []

    tweet_df['2gram'] = tweet_df[TWEET_META.TEXT_CLEANED].map(twogram)

    texts = list(tweet_df['2gram'])
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    lda = models.LdaModel(corpus, id2word=dictionary, num_topics=size)

    topic_keywords = self.get_topic_keywords(lda)

    df_topic_sents_keywords = self.format_topics_sentences(ldamodel=lda, corpus=corpus, texts=tweet_df[TWEET_META.TEXT_CLEANED], dates=tweet_df[TWEET_META.DATE])
    df_dominant_topic = df_topic_sents_keywords.reset_index()
    df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text', 'Date']
    topic_distribution = []
    topic_counts = []

    for topic_count in range(size):
      df_dominant_topic_item = df_dominant_topic[df_dominant_topic.Dominant_Topic == topic_count]
      topic_counts.append(len(df_dominant_topic_item))
      df_dominant_topic_item = df_dominant_topic_item.sort_values(by='Topic_Perc_Contrib', ascending=False).iloc[:10][['Date', 'Text', 'Topic_Perc_Contrib']]
      topic_distribution.append({
        'date': list(df_dominant_topic_item.Date),
        'text': list(df_dominant_topic_item.Text),
        'score': list(df_dominant_topic_item.Topic_Perc_Contrib)
      })
    return topic_keywords, topic_distribution, topic_counts


  def format_topics_sentences(self, ldamodel, corpus, texts, dates):
    # Init output
    sent_topics_df = pd.DataFrame()

    # Get main topic in each document
    for i, row_list in enumerate(ldamodel[corpus]):
        row = row_list[0] if ldamodel.per_word_topics else row_list            
        # print(row)
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # Add original text to the end of the output
    contents = pd.Series(texts)
    dates = pd.Series(dates)
    sent_topics_df = pd.concat([sent_topics_df, contents, dates], axis=1)
    return(sent_topics_df)

  def get_topic_keywords(self, lda):
    topic_words = lda.print_topics(10,10)

    def sep_topic_keywords(topic_item):
        topic = topic_item[0]
        keywords = topic_item[1].split(" + ")
        keywords_result = []
        for keyword in keywords:
            score_words = keyword.split("*\"")
            score_words[1] = score_words[1][:-1]
            keywords_result.append(score_words)
        return [topic, keywords_result]

    result = []

    for topic_item in topic_words:
        result.append(sep_topic_keywords(topic_item))

    return result