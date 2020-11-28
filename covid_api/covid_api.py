from flask import Flask, abort, request, jsonify
from utils.spark_util import spark
from datetime import datetime
from service.tweet_sentiment_service import TweetSentimentService
from service.hot_topic_service import HotTopicService
from service.covid_data_service import CovidDataService

app = Flask(__name__)

collection_uri = "mongodb://hkust:hkustAb$13gid@52.229.166.95:27017/MSBD5003.tweets_cleand?authSource=admin"
collection_data_uri = "mongodb://hkust:hkustAb$13gid@52.229.166.95:27017/MSBD5003.covid_data?authSource=admin"
collection_predict_uri = "mongodb://hkust:hkustAb$13gid@52.229.166.95:27017/MSBD5003.covid_prediction?authSource=admin"

tweet_sentiment_service = TweetSentimentService(collection_uri, spark)
tweet_topic_service = HotTopicService(collection_uri, spark)
covid_data_service = CovidDataService(collection_predict_uri, collection_data_uri, spark)

@app.route('/api/sentiment_analysis/info', methods=['GET'])
def sentiment_info():
    if not request.args or 'date_from' not in request.args or 'date_to' not in request.args:
        return {'result': 'not found'}

    else:
        date_from = request.args['date_from']
        date_to = request.args['date_to']
        keywords = request.args['keywords'].split("|") if request.args['keywords'] != "" else []
        print(keywords)
        print(len(keywords))

        if (datetime.strptime(date_to, "%Y-%m-%d") - datetime.strptime(date_from, "%Y-%m-%d")).days > 10:
            return {'result': 'date range too big, should be less or equal to 10'}

        result = tweet_sentiment_service.info(date_from, date_to, keywords)
        return result


@app.route('/api/topic/info', methods=['GET'])
def topic_info():
    if not request.args or 'date_from' not in request.args or 'date_to' not in request.args:
        return {'result': 'not found'}

    else:
        date_from = request.args['date_from']
        date_to = request.args['date_to']
        similar_sentence = request.args['similar_sentence']
        keywords = request.args['keywords'].split("|") if request.args['keywords'] != "" else []

        if (datetime.strptime(date_to, "%Y-%m-%d") - datetime.strptime(date_from, "%Y-%m-%d")).days > 10:
            return {'result': 'date range too big, should be less or equal to 10'}

        result = tweet_topic_service.info(date_from, date_to, keywords, similar_sentence)
        return result

@app.route('/api/covid_data/info', methods=['GET'])
def covid_data_info():
    if not request.args or 'date_from' not in request.args or 'date_to' not in request.args:
        return {'result': 'not found'}

    else:
        date_from = request.args['date_from']
        date_to = request.args['date_to']
        regions = request.args['regions'].split("|") if request.args['regions'] != "" else []

        if (datetime.strptime(date_to, "%Y-%m-%d") - datetime.strptime(date_from, "%Y-%m-%d")).days > 300:
            return {'result': 'date range too big, should be less or equal to 10'}

        result = covid_data_service.info(date_from, date_to, regions)
        return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8884, debug=True)