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
# to co trafia z kafki przychodzi w postaci binarnej więc trzeba przetworzyć to na string

(df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
 .writeStream
 .format("console")
 .outputMode("append")
 .start()
 .awaitTermination()
)

