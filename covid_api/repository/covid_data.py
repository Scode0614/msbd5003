class CovidDataRepository:
  def __init__(self, collection_prediction_uri: str, collection_data_uri: str, spark):
    self.df_covid_data = spark.read.format("mongo").option("uri", collection_data_uri).load()
    self.df_covid_prediction = spark.read.format("mongo").option("uri", collection_prediction_uri).load()
    

  ################################################################################################
  # Get Tweets from DB within the given date range
  # Inputs:
  # 1) from_date: YYYY-MM-DD, e.g: 2020-01-01
  # 2) to_date: YYYY-MM-DD, e.g: 2020-01-01
  # 3) country_name: e.g. China
  # Return:
  #   SparkSQL DataFrame
  ################################################################################################
  def get_covid_data_by_dates_and_country(self, from_date: str, to_date: str, country_name: str):
    return self.df_covid_data.where("date <= '" + to_date + "' and date >= '" + from_date + "' and location = '" + country_name + "'") \
      .select('location', 'date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'icu_patients', 'hosp_patients', 'total_tests', 'new_tests', 'positive_rate').toPandas()
  
  ################################################################################################
  # Get Tweets from DB within the given date range
  # Inputs:
  # 1) from_date: YYYY-MM-DD, e.g: 2020-01-01
  # 2) to_date: YYYY-MM-DD, e.g: 2020-01-01
  # Return:
  #   SparkSQL DataFrame
  ################################################################################################
  def get_covid_data_by_dates(self, from_date: str, to_date: str):
    return self.df_covid_data.where("date <= '" + to_date + "' and date >= '" + from_date + "'") \
      .select('location', 'date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'icu_patients', 'hosp_patients', 'total_tests', 'new_tests', 'positive_rate').toPandas()
  
  ################################################################################################
  # Get Tweets from DB within the given date range
  # Inputs:
  # 1) from_date: YYYY-MM-DD, e.g: 2020-01-01
  # 2) to_date: YYYY-MM-DD, e.g: 2020-01-01
  # 3) country_name: e.g. China
  # Return:
  #   SparkSQL DataFrame
  ################################################################################################
  def get_covid_prediction_by_dates_and_regions(self, from_date: str, to_date: str, regions: list):
    df = None
    for region in regions:
      df1 = self.df_covid_prediction.where("date <= '" + to_date + "' and date >= '" + from_date + "' and location = '" + region + "'") \
      .select('location', 'date', 'real_cases', 'predicted_cases', 'real_deaths', 'predicted_deaths')
      
      if df == None:
        df = df1
      else:
        df = df.unionAll(df1)

    return df.toPandas()
  
  ################################################################################################
  # Get Tweets from DB within the given date range
  # Inputs:
  # 1) from_date: YYYY-MM-DD, e.g: 2020-01-01
  # 2) to_date: YYYY-MM-DD, e.g: 2020-01-01
  # Return:
  #   SparkSQL DataFrame
  ################################################################################################
  def get_covid_prediction_by_dates(self, from_date: str, to_date: str):
    return self.df_covid_prediction.where("date <= '" + to_date + "' and date >= '" + from_date + "'") \
      .select('location', 'date', 'real_cases', 'predicted_cases', 'real_deaths', 'predicted_deaths').toPandas()
  


class META_PREDICTION(str):
  location = 'location'
  date = 'date'
  real_cases = 'real_cases'
  predicted_cases = 'predicted_cases'
  real_deaths = 'real_deaths'
  predicted_deaths = 'predicted_deaths'

class META_DATA(str):
  location = 'location'
  date = 'date'
  total_cases = 'total_cases'
  new_cases = 'new_cases'
  total_deaths = 'total_deaths'
  new_deaths = 'new_deaths'
  icu_patients = 'icu_patients'
  hosp_patients = 'hosp_patients'
  total_tests = 'total_tests'
  new_tests = 'new_tests'
  positive_rate = 'positive_rate'