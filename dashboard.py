import streamlit as st
import pandas as pd
import plotly.express as px
import pickle

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Dashboard") \
    .getOrCreate()

st.title("Smart Retail Visitor Prediction")

visitor_total = spark.read.parquet(
    "output/visitor_total"
).toPandas()

visitor_time = spark.read.parquet(
    "output/visitor_time"
).toPandas()

model = pickle.load(
    open("model.pkl", "rb")
)

zone = st.selectbox(
    "Pilih Zona",
    visitor_total["zone"]
)

selected = visitor_total[
    visitor_total["zone"] == zone
]

st.metric(
    "Total Visitor",
    int(selected["total_visitors"].values[0])
)

trend = visitor_time[
    visitor_time["zone"] == zone
]

fig = px.line(
    trend,
    x="minute_group",
    y="visitor_count",
    title="Trend Visitor"
)

st.plotly_chart(fig)

hour = st.slider(
    "Pilih Jam",
    0,
    23,
    12
)

prediction = model.predict(
    [[hour]]
)

st.subheader(
    f"Prediksi Visitor : {int(prediction[0])}"
)

spark.stop()