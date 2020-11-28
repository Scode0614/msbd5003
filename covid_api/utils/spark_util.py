from pyspark.sql import SparkSession
import sparknlp

import pyspark
from pyspark import SparkContext
from pyspark import SparkConf
spark = SparkSession.builder.master("local[1]").appName("covid_analysis.com").getOrCreate() 