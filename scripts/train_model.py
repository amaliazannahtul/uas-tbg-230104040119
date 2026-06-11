import pandas as pd
from sklearn.linear_model import LinearRegression
from pyspark.sql import SparkSession
import pickle

spark = SparkSession.builder \
    .appName("TrainModel") \
    .getOrCreate()

df = spark.read.parquet(
    "output/ml_visitor"
)

pdf = df.toPandas()

X = pdf[["hour"]]
y = pdf["visitor_count"]

model = LinearRegression()

model.fit(X, y)

pickle.dump(
    model,
    open("model.pkl", "wb")
)

print("MODEL BERHASIL DIBUAT")

spark.stop()