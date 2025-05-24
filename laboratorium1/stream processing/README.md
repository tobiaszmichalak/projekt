# Apache Kafka - Wprowadzenie

Apache Kafka to system przetwarzania strumieniowego (event streaming), który działa jako rozproszony broker wiadomości. 
Pozwala na przesyłanie i przetwarzanie danych w czasie rzeczywistym.

Domyślnym adresem naszego brokera jest `broker:9092`.

W Apache Kafka dane są przechowywane w strukturach zwanych **topicami**, które pełnią funkcję kolejek komunikacyjnych.

Zarządzanie Kafką odbywa się za pomocą skryptów. W naszym przypadku będą to skrypty `.sh`.

## 1️⃣ Sprawdź listę topiców
Pamiętaj, aby przejść do katalogu domowego:
```sh
cd ~
kafka/bin/kafka-topics.sh --list --bootstrap-server broker:9092
```

### 2️⃣ Utwórz nowy topic o nazwie `mytopic`
```sh
kafka/bin/kafka-topics.sh --create --topic mytopic --bootstrap-server broker:9092
```

### 3️⃣ Utwórz producenta
Ten skrypt pozwoli Ci wprowadzać eventy ręcznie przez terminal. Opcje `--property` są dodatkowe i służą do analizy w tym przykładzie.
```sh
kafka/bin/kafka-console-producer.sh --bootstrap-server broker:9092 --topic mytopic --property "parse.key=true" --property "key.separator=:"
```

### 4️⃣ Consumer w Sparku
Otwórz nowy terminal w miejscu, gdzie znajduje się plik `test_key_value.py`, i uruchom program **Consumer**a w Sparku.

```python
from pyspark.sql import SparkSession

KAFKA_BROKER = 'broker:9092'
KAFKA_TOPIC = 'mytopic'

spark = SparkSession.builder.getOrCreate()
spark.sparkContext.setLogLevel("WARN")

df = (spark.readStream.format("kafka")
      .option("kafka.bootstrap.servers", KAFKA_BROKER)
      .option("subscribe", KAFKA_TOPIC)
      .option("startingOffsets", "earliest")
      .load()
     )

# Konwersja danych binarnych na stringi
df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
 .writeStream \
 .format("console") \
 .outputMode("append") \
 .start() \
 .awaitTermination()
```

Pamiętaj, że Apache Spark nie posiada domyślnego konektora do Kafki, dlatego uruchom proces za pomocą `spark-submit` i pobierz odpowiedni pakiet w Scali:
```sh
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 test_key_value.py
```

### 5️⃣ Przetestuj przesyłanie danych
W terminalu z uruchomionym producentem wpisz tekst w postaci:
```bash
jan:45
alicja:20
```

Sprawdź, co pojawia się w oknie aplikacji Consumera.

### 6️⃣ Zakończenie procesu
Po zakończeniu pokazu użyj `Ctrl+C`, aby zamknąć zarówno okno producenta, jak i aplikację Spark.

---
Gotowe! Teraz masz podstawową konfigurację Apache Kafka i Spark do analizy strumieniowej. 🎉

