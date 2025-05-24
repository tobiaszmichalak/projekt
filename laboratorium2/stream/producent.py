
import json
import random
from datetime import datetime
from time import sleep
from kafka import KafkaProducer

SERVER = "broker:9092"
TOPIC = "mytopic"

if __name__ == "__main__":
    

    producer = KafkaProducer(
        bootstrap_servers=[SERVER],
        value_serializer=lambda x: json.dumps(x).encode("utf-8"),
    )
    
    try:
        while True:
            
            t = datetime.now()
            
            message = {
                "time" : str(t),
                "id" : random.choice(["a", "b", "c", "d", "e"]),
                "values" : random.randint(0,100)
            }
            
            
            producer.send(TOPIC, value=message)
            sleep(1)
    except KeyboardInterrupt:
        producer.close()
