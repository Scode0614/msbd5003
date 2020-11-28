## preprocess
- **tweet.ipynb** is used to clean tweet text and generate sentiment label
- (others)

## analysis
- **topic_analysis.ipynb** (to be updated by Zhongyu)
- **sentiment_analysis.ipynb** (to be updated by Siting)
- **sir_model.ipynb** (to be updated by Tangchun)

## covid_api
- run **covid_api.py** to start the server on localhost:8884
- **repository** folder includes SparkSQL code to access Database for tweets and covid data
- **service** folder includes 3 service classes for topic / sentiment / covid data analysis, to be used in web app

## covid_ui
- use and design pro frameword: https://pro.ant.design/
- **src/pages** includes topic / sentiment / covid_data 3 pages
- **src/services** inncludes the api definition for each of 3 services
- **src/utils** utility functions for formatting data and generate chart