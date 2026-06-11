import pandas as pd
import random
from datetime import datetime, timedelta

start_time = datetime.now()

data = []

zones = [
    "FoodCourt",
    "FashionArea",
    "Cinema"
]

for i in range(180):

    timestamp = start_time + timedelta(minutes=i)

    zone = random.choice(zones)

    visitor_count = random.randint(10, 500)

    data.append([
        timestamp,
        zone,
        visitor_count
    ])

df = pd.DataFrame(
    data,
    columns=[
        "timestamp",
        "zone",
        "visitor_count"
    ]
)

df.to_csv(
    "data/visitor_data.csv",
    index=False
)

print(df.head())