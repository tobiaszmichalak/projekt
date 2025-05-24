
from kafka import KafkaConsumer
import json

SERVER = "broker:9092"
TOPIC = "mytopic"

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=SERVER,
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    data = message.value
    alerts = []

    if data.get("TotalSteps", 0) > 15000:
        alerts.append("🚶‍♂️ Nadzwyczajna ilość kroków!")

    if data.get("Calories", 0) > 4000:
        alerts.append("🔥 Nietypowo wysokie spalanie kalorii!")

    if data.get("VeryActiveMinutes", 0) > 120:
        alerts.append("⏱️ Bardzo długi okres intensywnej aktywności!")

    print(f"Odebrano: {data}")
    if alerts:
        for alert in alerts:
            print(f"  ⚠️ ALERT: {alert}")
