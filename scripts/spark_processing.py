from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder \
    .appName("RetailVisitorAnalytics") \
    .getOrCreate()

df = spark.read.csv(
    "data/visitor_data.csv",
    header=True,
    inferSchema=True
)

df = df.withColumn(
    "hour",
    hour(col("timestamp"))
)

df = df.withColumn(
    "minute_group",
    floor(minute(col("timestamp")) / 15) * 15
)

# 1 Total visitor per zone

visitor_total = df.groupBy(
    "zone"
).agg(
    sum("visitor_count").alias("total_visitors")
)

# 2 Trend per 15 menit

visitor_time = df.groupBy(
    "zone",
    "hour",
    "minute_group"
).agg(
    sum("visitor_count").alias("visitor_count")
)

# 3 Dataset ML

ml_dataset = df.select(
    "hour",
    "visitor_count"
)

visitor_total.write.mode("overwrite").parquet(
    "output/visitor_total"
)

visitor_time.write.mode("overwrite").parquet(
    "output/visitor_time"
)

ml_dataset.write.mode("overwrite").parquet(
    "output/ml_visitor"
)

print("PARQUET BERHASIL DIBUAT")

spark.stop()