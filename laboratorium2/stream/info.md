## 1️⃣ Sprawdź listę topiców
Pamiętaj, aby przejść do katalogu domowego:
```sh
cd ~
kafka/bin/kafka-topics.sh --list --bootstrap-server broker:9092
```

## 2️⃣ Utwórz nowy topic o nazwie `mytopic`
```sh
kafka/bin/kafka-topics.sh --create --topic mytopic --bootstrap-server broker:9092
```

## 3 sprawdź czy topic istnieje 
```sh
kafka/bin/kafka-topics.sh --list --bootstrap-server broker:9092 | grep mytopic
```
