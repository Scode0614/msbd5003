from repository.covid_data import CovidDataRepository
from repository.covid_data import META_PREDICTION
from repository.covid_data import META_DATA

import numpy as np
import pandas as pd

class CovidDataService:
  def __init__(self, collection_predict_uri: str, collection_data_uri: str, spark):
    self.covid_data_repo = CovidDataRepository(collection_predict_uri, collection_data_uri, spark)

  def info(self, from_date: str, to_date: str, regions: list):
    covid_data_list = self.get_data_list(from_date, to_date)
    covid_predict_list = self.get_predict_list(from_date, to_date, regions)
    return {
      'covid_data_list': covid_data_list,
      'covid_predict_list': covid_predict_list
    }

  def get_data_list(self, from_date: str, to_date: str):
    df = self.covid_data_repo.get_covid_data_by_dates(from_date, to_date)

    list_attributes = [META_DATA.location, META_DATA.date, META_DATA.location, META_DATA.date,
      META_DATA.total_cases, META_DATA.new_cases, META_DATA.total_deaths,
      META_DATA.new_deaths, META_DATA.icu_patients, META_DATA.hosp_patients,
      META_DATA.total_tests, META_DATA.new_tests, META_DATA.positive_rate]

    def format(x):
      if not pd.notnull(x):
          return ''
      else:
          return x

    result = {}

    for attribute in list_attributes:
      if attribute != META_DATA.location and attribute != META_DATA.date:
        df[attribute] = df[attribute].map(format)
      result[attribute] = list(df[attribute])
  
    return result

  def get_predict_list(self, from_date: str, to_date: str, regions: list):
    df = self.covid_data_repo.get_covid_prediction_by_dates_and_regions(from_date, to_date, regions)
    
    return {
      META_PREDICTION.location: list(df[META_PREDICTION.location]),
      META_PREDICTION.date: list(df[META_PREDICTION.date]),
      META_PREDICTION.real_cases: list(df[META_PREDICTION.real_cases]),
      META_PREDICTION.predicted_cases: list(df[META_PREDICTION.predicted_cases]),
      META_PREDICTION.real_deaths: list(df[META_PREDICTION.real_deaths]),
      META_PREDICTION.predicted_deaths: list(df[META_PREDICTION.predicted_deaths]),
    }