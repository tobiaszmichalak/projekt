
import pandas as pd
import json
import random
from datetime import datetime, timedelta
from time import sleep
from kafka import KafkaProducer

# Kafka config
SERVER = "broker:9092"
TOPIC = "mytopic"

# Wczytaj dane z pliku CSV
df = pd.read_csv("dailyActivity_merged.csv")
df = df[['Id', 'ActivityDate', 'TotalSteps', 'Calories', 'VeryActiveMinutes']]

# Generowanie danych syntetycznych
def generate_synthetic_data(n=1000):
    base_date = datetime(2023, 1, 1)
    synthetic = []
    for i in range(n):
        entry = {
            "Id": random.randint(1000000000, 9999999999),
            "ActivityDate": (base_date + timedelta(days=i % 365)).strftime("%m/%d/%Y"),
            "TotalSteps": random.randint(0, 25000),
            "Calories": random.randint(1500, 5000),
            "VeryActiveMinutes": random.randint(0, 180)
        }
        synthetic.append(entry)
    return pd.DataFrame(synthetic)

if len(df) < 1000:
    synthetic_df = generate_synthetic_data(n=1000 - len(df))
    df = pd.concat([df, synthetic_df], ignore_index=True)

# Konfiguracja producenta Kafka
producer = KafkaProducer(
    bootstrap_servers=[SERVER],
    value_serializer=lambda x: json.dumps(x).encode("utf-8"),
)

try:
    while True:
        sample = df.sample(1).to_dict(orient="records")[0]
        producer.send(TOPIC, value=sample)
        print(f"Wysłano: {sample}")
        sleep(1)
except KeyboardInterrupt:
    producer.close()
