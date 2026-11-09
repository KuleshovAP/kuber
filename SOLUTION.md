# Kafka, CI/CD и Kubernetes — исправленная версия

Автор: Кулешов Алексей Петрович.

## Исправления по замечаниям

1. Зависимости находятся в **app/requirements.txt**, корневого requirements.txt в этой поставке нет. Dockerfile и CI обновлены.
2. Подготовлены CI-файлы для GitHub и GitLab. Наличие настоящего репозитория подтверждается только ссылкой и commit ниже.
3. Добавлен **kafka-demo-deployment.yaml** с **kind: Deployment**. Приложение имеет постоянный режим и readiness после реального обмена.
4. Требуемая среда — Kubernetes, включённый в интерфейсе **Docker Desktop**, контекст **docker-desktop**. Прежний отдельный kind-кластер не считается подтверждением этого пункта.

## Репозиторий

[Проект](https://github.com/KuleshovAP/kuber)

Commit с проверенными исходниками: `16ada2876f3f4c704af35281e4f0e8eee110a5e0`. Отчёт дополняется отдельными документационными commit.

GitHub Actions: [подтверждённый запуск](https://github.com/KuleshovAP/kuber/actions/runs/42649184940), результат **success**.

## Подтверждение запуска

Только журналы **этой версии** ниже подтверждают выполненные проверки. Включение настройки без Ready Deployment не считается успешным запуском приложения.

### evidence/ci-run.json

````text
{
  "id": 42649184940,
  "html_url": "https://github.com/KuleshovAP/kuber/actions/runs/42649184940",
  "name": "Kafka application CI",
  "head_sha": "16ada2876f3f4c704af35281e4f0e8eee110a5e0",
  "status": "completed",
  "conclusion": "success",
  "created_at": "2026-11-09T15:53:27Z",
  "updated_at": "2026-11-09T15:54:11Z"
}

````

### evidence/desktop-compose-stop.log

````text
docker :  Container kafka-homework-kafka-1 Stopping 
строка:2 знак:94
+ ... +$env:PATH; docker compose stop kafka zookeeper *> evidence/desktop-c ...
+                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: ( Container kafk...fka-1 Stopping :String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
 Container kafka-homework-kafka-1 Stopped 
 Container kafka-homework-zookeeper-1 Stopping 
 Container kafka-homework-zookeeper-1 Stopped 

````

### evidence/desktop-final-state.log

````text
Field               Value
ID:                 2ca086a9
State:              running
Mode:               kind
Node Count:         2
Version:            1.36.1
Started At:         2026-11-09 18:39:29.182 +0300 MSK
Progress Message:   Kubernetes is up and running
Error:              None
NAME                         READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/kafka-demo   1/1     1            1           4m15s

NAME                              READY   STATUS    RESTARTS   AGE
pod/kafka-0                       1/1     Running   0          5m47s
pod/kafka-1                       1/1     Running   0          5m47s
pod/kafka-2                       1/1     Running   0          5m47s
pod/kafka-demo-79c5c8b55f-8bwmv   1/1     Running   0          4m14s
pod/zookeeper-0                   1/1     Running   0          5m47s
{"topic": "demo-2e702d39abfe4ab884b516854335eb5e", "partition": 0, "offset": 0, "received": {"event_id": "4643046f01044906852ca5928cf3c50f", "message": "Hello, Kafka!", "value": 42}}
{"topic": "demo-bdd5a3d80cc94486ae93712ca4efce19", "partition": 0, "offset": 0, "received": {"event_id": "83166775780d4cebac05da3a416a8755", "message": "Hello, Kafka!", "value": 42}}
{"topic": "demo-5e49795faf864de98fd289c57d4942a7", "partition": 0, "offset": 0, "received": {"event_id": "bc593ccab5474d8695e244ae27115334", "message": "Hello, Kafka!", "value": 42}}

````

### evidence/docker-desktop-deployment.log

````text
Field               Value
ID:                 2ca086a9
State:              running
Mode:               kind
Node Count:         2
Version:            1.36.1
Started At:         2026-11-09 18:39:29.182 +0300 MSK
Progress Message:   Kubernetes is up and running
Error:              None
Kubernetes control plane is running at https://127.0.0.1:62830
CoreDNS is running at https://127.0.0.1:62830/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
NAME                    STATUS   ROLES           AGE   VERSION
desktop-control-plane   Ready    control-plane   85s   v1.36.1
desktop-worker          Ready    <none>          71s   v1.36.1
namespace/kafka-homework created
service/zookeeper created
statefulset.apps/zookeeper created
service/kafka-headless created
service/kafka created
statefulset.apps/kafka created
Waiting for 1 pods to be ready...
partitioned roll out complete: 1 new pods have been updated...
Waiting for 3 pods to be ready...
Waiting for 2 pods to be ready...
Waiting for 1 pods to be ready...
partitioned roll out complete: 3 new pods have been updated...
deployment.apps/kafka-demo created
Waiting for deployment spec update to be observed...
Waiting for deployment "kafka-demo" rollout to finish: 0 of 1 updated replicas are available...
deployment "kafka-demo" successfully rolled out
NAME                         READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/kafka-demo   1/1     1            1           12s

NAME                              READY   STATUS    RESTARTS   AGE
pod/kafka-0                       1/1     Running   0          104s
pod/kafka-1                       1/1     Running   0          104s
pod/kafka-2                       1/1     Running   0          104s
pod/kafka-demo-79c5c8b55f-8bwmv   1/1     Running   0          11s
pod/zookeeper-0                   1/1     Running   0          104s

NAME                                        STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
persistentvolumeclaim/kafka-data-kafka-0    Bound    pvc-bdbc7da3-df09-4b40-bf11-441902d51193   2Gi        RWO            standard       <unset>                 104s
persistentvolumeclaim/kafka-data-kafka-1    Bound    pvc-837579b4-fa28-4096-9a70-fb28609275ae   2Gi        RWO            standard       <unset>                 104s
persistentvolumeclaim/kafka-data-kafka-2    Bound    pvc-7d5b446d-922c-490a-a733-d31f212d0f2a   2Gi        RWO            standard       <unset>                 104s
persistentvolumeclaim/zk-data-zookeeper-0   Bound    pvc-a4f19d16-9ace-424b-ad0c-bc99247aa3e1   1Gi        RWO            standard       <unset>                 104s
{"topic": "demo-de67cd32443b40728d70cbd113da16ce", "partition": 0, "offset": 0, "received": {"event_id": "29e094919ade43ee9a68828750cbbe0f", "message": "Hello, Kafka!", "value": 42}}

````

### evidence/revision-app-build.log

````text
docker :  Image kafka-homework-app:local Building 
строка:2 знак:252
+ ... 15;exit 1}; docker compose build app *> evidence/revision-app-build.l ...
+                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: ( Image kafka-ho...local Building :String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
#1 [internal] load local bake definitions
#1 reading from stdin 684B 0.0s done
#1 DONE 0.0s

#2 [internal] load build definition from Dockerfile
#2 transferring dockerfile: 30B 0.0s
#2 transferring dockerfile: 278B 0.1s done
#2 DONE 0.2s

#3 [internal] load metadata for docker.io/library/python:3.11.11-slim-bookworm
#3 DONE 8.0s

#4 [internal] load .dockerignore
#4 transferring context: 97B done
#4 DONE 0.0s

#5 [internal] load build context
#5 transferring context: 1.36kB 0.0s done
#5 DONE 0.1s

#6 [1/6] FROM docker.io/library/python:3.11.11-slim-bookworm@sha256:081075da77b2b55c23c088251026fb69a7b2bf92471e491ff5fd75c192fd38e5
#6 resolve docker.io/library/python:3.11.11-slim-bookworm@sha256:081075da77b2b55c23c088251026fb69a7b2bf92471e491ff5fd75c192fd38e5
#6 resolve docker.io/library/python:3.11.11-slim-bookworm@sha256:081075da77b2b55c23c088251026fb69a7b2bf92471e491ff5fd75c192fd38e5 0.1s done
#6 DONE 0.1s

#7 [2/6] WORKDIR /app
#7 CACHED

#8 [3/6] COPY app/requirements.txt app/requirements.txt
#8 CACHED

#9 [4/6] RUN pip install --no-cache-dir -r app/requirements.txt
#9 CACHED

#10 [5/6] COPY app/ app/
#10 DONE 0.2s

#11 [6/6] COPY tests/ tests/
#11 DONE 0.1s

#12 exporting to image
#12 exporting layers
#12 exporting layers 0.7s done
#12 exporting manifest sha256:94f05f7ada4f307b1a556e5f5a4a60b9f978eb4c9ff53e4dc44abbba145a4c7e 0.1s done
#12 exporting config sha256:d383d29b6d5a09a80d92c5d6481cd8b856f596fcea47049fd47a40ae51f6d3a9 0.0s done
#12 naming to docker.io/library/kafka-homework-app:local 0.0s done
#12 unpacking to docker.io/library/kafka-homework-app:local
#12 unpacking to docker.io/library/kafka-homework-app:local 0.2s done
#12 DONE 1.0s

#13 resolving provenance for metadata file
#13 DONE 0.1s
 Image kafka-homework-app:local Built 

````

### evidence/revision-compose-up.log

````text
docker : time="2026-11-09T18:42:18+03:00" level=warning msg="Found orphan containers (kafka-homework-kafka-custom-1, ka
fka-homework-zookeeper-custom-1, kafka-homework-kafka-exporter-1, kafka-homework-prometheus-1, kafka-homework-grafana-1
) for this project. If you removed or renamed this service in your compose file, you can run this command with the --re
move-orphans flag to clean it up."
строка:2 знак:94
+ ... +$env:PATH; docker compose up -d --wait kafka *> evidence/revision-co ...
+                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (time="2026-11-0...o clean it up.":String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
 Container kafka-homework-zookeeper-1 Starting 
 Container kafka-homework-zookeeper-1 Started 
 Container kafka-homework-kafka-1 Starting 
 Container kafka-homework-kafka-1 Started 
 Container kafka-homework-kafka-1 Waiting 
 Container kafka-homework-zookeeper-1 Waiting 
 Container kafka-homework-zookeeper-1 Healthy 
 Container kafka-homework-kafka-1 Healthy 

````

### evidence/revision-tests.log

````text
docker : time="2026-11-09T18:42:55+03:00" level=warning msg="Found orphan containers (kafka-homework-kafka-custom-1, ka
fka-homework-zookeeper-custom-1, kafka-homework-kafka-exporter-1, kafka-homework-prometheus-1, kafka-homework-grafana-1
) for this project. If you removed or renamed this service in your compose file, you can run this command with the --re
move-orphans flag to clean it up."
строка:2 знак:414
+ ... esktop; & { docker compose run --rm app python -m pytest tests/unit t ...
+                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (time="2026-11-0...o clean it up.":String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
 Container kafka-homework-zookeeper-1 Running 
 Container kafka-homework-kafka-1 Running 
 Container kafka-homework-kafka-1 Waiting 
 Container kafka-homework-kafka-1 Healthy 
 Container kafka-homework-app-run-61bd05443ee7 Creating 
 Container kafka-homework-app-run-61bd05443ee7 Created 
============================= test session starts ==============================
platform linux -- Python 3.11.11, pytest-8.3.5, pluggy-1.7.0 -- /usr/local/bin/python
cachedir: .pytest_cache
rootdir: /app
collecting ... collected 2 items

tests/unit/test_kafka_client.py::test_event_preserves_unicode_and_numbers PASSED [ 50%]
tests/integration/test_integration.py::test_real_broker_roundtrip PASSED [100%]

============================== 2 passed in 0.83s ===============================
docker : time="2026-11-09T18:42:59+03:00" level=warning msg="Found orphan containers (kafka-homework-kafka-custom-1, ka
fka-homework-zookeeper-custom-1, kafka-homework-kafka-exporter-1, kafka-homework-prometheus-1, kafka-homework-grafana-1
) for this project. If you removed or renamed this service in your compose file, you can run this command with the --re
move-orphans flag to clean it up."
строка:2 знак:532
+ ... STEXITCODE -ne 0){throw 'tests'}; docker compose run --rm app; if($LA ...
+                                       ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (time="2026-11-0...o clean it up.":String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
 Container kafka-homework-zookeeper-1 Running 
 Container kafka-homework-kafka-1 Running 
 Container kafka-homework-kafka-1 Waiting 
 Container kafka-homework-kafka-1 Healthy 
 Container kafka-homework-app-run-124b4679d4ef Creating 
 Container kafka-homework-app-run-124b4679d4ef Created 
{"topic": "demo-25802347cb484d31bdd09c5198b6f5f6", "partition": 0, "offset": 0, "received": {"event_id": "dc6697b6ccde488fa12eb0f91f4aa9be", "message": "Hello, Kafka!", "value": 42}}

````

### evidence/revision-unit.log

````text
============================= test session starts ==============================
platform linux -- Python 3.11.11, pytest-8.3.5, pluggy-1.7.0 -- /usr/local/bin/python
cachedir: .pytest_cache
rootdir: /app
collecting ... collected 1 item

tests/unit/test_kafka_client.py::test_event_preserves_unicode_and_numbers PASSED [100%]

============================== 1 passed in 0.16s ===============================

````

## Назначение и полное содержимое файлов

### app/requirements.txt

Обязательный список зависимостей внутри app: kafka-python и pytest. Именно этот путь используется Dockerfile и обоими вариантами CI.

````text
kafka-python==2.2.15
pytest==8.3.5

````

### app/__init__.py

Объявляет Python-пакет app.

````text
"""Учебное приложение Kafka."""

````

### app/kafka_client.py

Создаёт уникальный topic, отправляет UTF-8 JSON с acks=all, читает с earliest с тайм-аутом и сверяет событие. В finally закрывает клиентов и удаляет временный topic. Replication factor берётся из окружения: 1 в Compose, 3 в Kubernetes.

````text
"""Ограниченный по времени обмен JSON-сообщениями через Kafka."""
import json
import os
import uuid

from kafka import KafkaConsumer, KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError


def encode_event(event):
    return json.dumps(event, ensure_ascii=False).encode('utf-8')


def roundtrip(broker=None):
    broker = broker or os.environ.get('KAFKA_BROKER', 'localhost:9092')
    replication = int(os.environ.get('KAFKA_REPLICATION_FACTOR', '1'))
    # Отдельный topic на проверку исключает чтение старого сообщения.
    topic = 'demo-' + uuid.uuid4().hex
    admin = KafkaAdminClient(bootstrap_servers=broker, request_timeout_ms=20000)
    producer = consumer = None
    try:
        try:
            admin.create_topics([NewTopic(topic, 1, replication)])
        except TopicAlreadyExistsError:
            pass
        event = {'event_id': uuid.uuid4().hex, 'message': 'Hello, Kafka!', 'value': 42}
        producer = KafkaProducer(bootstrap_servers=broker, value_serializer=encode_event, acks='all')
        metadata = producer.send(topic, event).get(timeout=30)
        producer.flush(timeout=30)
        consumer = KafkaConsumer(
            topic, bootstrap_servers=broker, auto_offset_reset='earliest',
            enable_auto_commit=False, group_id=None, consumer_timeout_ms=30000,
            value_deserializer=lambda data: json.loads(data.decode('utf-8')),
        )
        for record in consumer:
            if record.value == event:
                return {'topic': topic, 'partition': metadata.partition,
                        'offset': metadata.offset, 'received': record.value}
        raise TimeoutError('Сообщение не получено за 30 секунд')
    finally:
        if consumer is not None:
            consumer.close()
        if producer is not None:
            producer.close(timeout=10)
        # Тестовые topic не накапливаются между запусками.
        try:
            admin.delete_topics([topic], timeout_ms=10000)
        finally:
            admin.close()

````

### app/main.py

Точка входа. По умолчанию выполняет один обмен; --continuous оставляет приложение работающим и повторяет обмен. Readiness-маркер появляется после успешного получения сообщения.

````text
"""Однократная демонстрация producer -> broker -> consumer."""
import json
import argparse
import time
from pathlib import Path
from app.kafka_client import roundtrip

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--continuous', action='store_true',
                        help='Периодический обмен для постоянного Deployment')
    parser.add_argument('--interval', type=float, default=30)
    args = parser.parse_args()
    if args.interval <= 0:
        parser.error('interval должен быть положительным')
    while True:
        print(json.dumps(roundtrip(), ensure_ascii=False), flush=True)
        if not args.continuous:
            break
        # Readiness включается только после реального обмена с брокером.
        Path('/tmp/kafka-demo-ready').touch()
        time.sleep(args.interval)

````

### Dockerfile

Корневой Dockerfile Python 3.11.11: копирует app/requirements.txt, устанавливает зависимости именно из него, затем копирует app и tests. Запускает python -m app.main.

````text
FROM python:3.11.11-slim-bookworm
WORKDIR /app
COPY app/requirements.txt app/requirements.txt
RUN pip install --no-cache-dir -r app/requirements.txt
COPY app/ app/
COPY tests/ tests/
ENV PYTHONUNBUFFERED=1
CMD ["python", "-m", "app.main"]

````

### docker-compose.yml

Kafka 7.9.0 и ZooKeeper 7.9.0, постоянные тома, внутренний/внешний listeners и healthcheck Kafka. app запускается после готовности брокера. Provenance отключён для совместимости локального импорта образа.

````text
name: kafka-homework
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.9.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
      KAFKA_HEAP_OPTS: '-Xms128m -Xmx128m'
    volumes:
      - zk-data:/var/lib/zookeeper/data
      - zk-log:/var/lib/zookeeper/log
  kafka:
    image: confluentinc/cp-kafka:7.9.0
    depends_on:
      - zookeeper
    ports:
      - '127.0.0.1:9092:9092'
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_HEAP_OPTS: '-Xms256m -Xmx256m'
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_LISTENERS: INTERNAL://0.0.0.0:29092,EXTERNAL://0.0.0.0:9092
      KAFKA_ADVERTISED_LISTENERS: INTERNAL://kafka:29092,EXTERNAL://localhost:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: INTERNAL
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
    healthcheck:
      test: ['CMD-SHELL', 'kafka-topics --bootstrap-server localhost:29092 --list >/dev/null 2>&1']
      interval: 10s
      timeout: 10s
      retries: 30
      start_period: 30s
    volumes:
      - kafka-data:/var/lib/kafka/data
  app:
    image: kafka-homework-app:local
    build:
      context: .
      # kind 0.27/containerd 2.0 импортирует обычный single-platform образ.
      provenance: false
    environment:
      KAFKA_BROKER: kafka:29092
    depends_on:
      kafka:
        condition: service_healthy
volumes:
  zk-data:
  zk-log:
  kafka-data:

````

### tests/unit/test_kafka_client.py

Проверяет сохранение Unicode и чисел при сериализации без брокера.

````text
import json
from app.kafka_client import encode_event


def test_event_preserves_unicode_and_numbers():
    event = {'message': 'Привет, Kafka!', 'value': 42}
    encoded = encode_event(event)
    assert isinstance(encoded, bytes)
    assert json.loads(encoded.decode('utf-8')) == event

````

### tests/integration/test_integration.py

Проверяет настоящий обмен с Kafka, текст, значение, partition и offset уникального topic.

````text
from app.kafka_client import roundtrip


def test_real_broker_roundtrip():
    result = roundtrip()
    assert result['received']['message'] == 'Hello, Kafka!'
    assert result['received']['value'] == 42
    assert result['partition'] == 0
    assert result['offset'] == 0

````

### .gitlab-ci.yml

GitLab pipeline со стадиями test/build/deploy: unit и integration, сборка/push по commit SHA, ручной deploy через deploy_script.sh.

````text
stages: [test, build, deploy]

unit_tests:
  stage: test
  image: python:3.11.11-slim-bookworm
  script:
    - pip install -r app/requirements.txt
    - python -m pytest tests/unit -v

integration_tests:
  stage: test
  image: docker:27.5.1-cli
  services:
    - name: docker:27.5.1-dind
      alias: docker
  variables:
    DOCKER_HOST: tcp://docker:2375
    DOCKER_TLS_CERTDIR: ''
  script:
    - docker compose up -d --wait kafka
    - docker compose build app
    - docker compose run --rm app python -m pytest tests/integration -v
  after_script:
    - docker compose logs --no-color > integration.log
    - docker compose down
  artifacts:
    when: always
    paths: [integration.log]

build:
  stage: build
  image: docker:27.5.1-cli
  services:
    - name: docker:27.5.1-dind
      alias: docker
  variables:
    DOCKER_HOST: tcp://docker:2375
    DOCKER_TLS_CERTDIR: ''
  script:
    - echo "$CI_REGISTRY_PASSWORD" | docker login "$CI_REGISTRY" --username "$CI_REGISTRY_USER" --password-stdin
    - docker build -t "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA" .
    - docker push "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA"

deploy:
  stage: deploy
  image:
    name: alpine/k8s:1.32.2
    entrypoint: ['']
  script:
    - sh deploy_script.sh "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA"
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
      when: manual

````

### .github/workflows/ci.yml

Рабочая конфигурация GitHub Actions для push/PR/manual: unit и integration с реальной Kafka, сборка Docker-образа и сохранение диагностики.

````text
name: Kafka application CI
on:
  push:
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  unit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r app/requirements.txt
      - run: python -m pytest tests/unit -v
  integration:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Start Kafka and build application
        run: |
          docker compose up -d --wait kafka
          docker compose build app
      - name: Test real Kafka exchange
        run: docker compose run --rm app python -m pytest tests/integration -v
      - name: Save diagnostics
        if: always()
        run: docker compose logs --no-color > integration.log
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: integration-log
          path: integration.log
      - name: Stop services
        if: always()
        run: docker compose down

````

### kafka-demo-deployment.yaml

Обязательный корневой манифест приложения: apps/v1 Deployment kafka-demo, одна реплика, постоянный процесс --continuous, readinessProbe после обмена с Kafka и ограничения ресурсов. Это не Job.

````text
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kafka-demo
  namespace: kafka-homework
  labels:
    app: kafka-demo
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kafka-demo
  template:
    metadata:
      labels:
        app: kafka-demo
    spec:
      enableServiceLinks: false
      containers:
        - name: kafka-demo
          image: kafka-homework-app:desktop
          imagePullPolicy: IfNotPresent
          command: ['python', '-m', 'app.main', '--continuous', '--interval', '30']
          env:
            - name: KAFKA_BROKER
              value: kafka:9092
            - name: KAFKA_REPLICATION_FACTOR
              value: '3'
          resources:
            requests:
              cpu: 50m
              memory: 64Mi
            limits:
              cpu: 500m
              memory: 256Mi
          readinessProbe:
            exec:
              command: ['test', '-f', '/tmp/kafka-demo-ready']
            initialDelaySeconds: 2
            periodSeconds: 3

````

### k8s/namespace.yaml

Отдельный namespace kafka-homework в выбранном контексте docker-desktop.

````text
apiVersion: v1
kind: Namespace
metadata:
  name: kafka-homework

````

### k8s/zookeeper.yaml

Headless Service и StatefulSet одиночного ZooKeeper с PVC 1 Gi и проверкой доступности TCP.

````text
apiVersion: v1
kind: Service
metadata:
  name: zookeeper
  namespace: kafka-homework
spec:
  clusterIP: None
  selector:
    app: zookeeper
  ports:
    - name: client
      port: 2181
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: zookeeper
  namespace: kafka-homework
spec:
  serviceName: zookeeper
  replicas: 1
  selector:
    matchLabels:
      app: zookeeper
  template:
    metadata:
      labels:
        app: zookeeper
    spec:
      containers:
        - name: zookeeper
          image: confluentinc/cp-zookeeper:7.9.0
          env:
            - name: ZOOKEEPER_CLIENT_PORT
              value: '2181'
            - name: ZOOKEEPER_TICK_TIME
              value: '2000'
            - name: KAFKA_HEAP_OPTS
              value: '-Xms128m -Xmx128m'
          ports:
            - containerPort: 2181
          readinessProbe:
            tcpSocket:
              port: 2181
            initialDelaySeconds: 10
          volumeMounts:
            - name: zk-data
              mountPath: /var/lib/zookeeper
  volumeClaimTemplates:
    - metadata:
        name: zk-data
      spec:
        accessModes: [ReadWriteOnce]
        resources:
          requests:
            storage: 1Gi

````

### k8s/kafka.yaml

Bootstrap Service, headless Service и StatefulSet трёх брокеров с PVC по 2 Gi. broker.id — числовой ordinal, advertised listener — DNS своего Pod. enableServiceLinks=false устраняет конфликт KAFKA_PORT.

````text
apiVersion: v1
kind: Service
metadata:
  name: kafka-headless
  namespace: kafka-homework
spec:
  clusterIP: None
  publishNotReadyAddresses: true
  selector:
    app: kafka
  ports:
    - name: kafka
      port: 9092
---
apiVersion: v1
kind: Service
metadata:
  name: kafka
  namespace: kafka-homework
spec:
  selector:
    app: kafka
  ports:
    - name: kafka
      port: 9092
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: kafka
  namespace: kafka-homework
spec:
  serviceName: kafka-headless
  replicas: 3
  podManagementPolicy: Parallel
  selector:
    matchLabels:
      app: kafka
  template:
    metadata:
      labels:
        app: kafka
    spec:
      # Иначе Service kafka создаёт KAFKA_PORT=tcp://..., конфликтующий
      # с устаревшей настройкой порта в Confluent entrypoint.
      enableServiceLinks: false
      containers:
        - name: kafka
          image: confluentinc/cp-kafka:7.9.0
          # broker.id должен быть числом: выделяем ordinal из имени Pod.
          command: ['/bin/bash', '-ec']
          args:
            - |
              export KAFKA_BROKER_ID="${HOSTNAME##*-}"
              export KAFKA_ADVERTISED_LISTENERS="PLAINTEXT://${HOSTNAME}.kafka-headless.kafka-homework.svc.cluster.local:9092"
              exec /etc/confluent/docker/run
          env:
            - name: KAFKA_ZOOKEEPER_CONNECT
              value: zookeeper:2181
            - name: KAFKA_LISTENERS
              value: PLAINTEXT://0.0.0.0:9092
            - name: KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR
              value: '3'
            - name: KAFKA_DEFAULT_REPLICATION_FACTOR
              value: '3'
            - name: KAFKA_MIN_INSYNC_REPLICAS
              value: '2'
            - name: KAFKA_HEAP_OPTS
              value: '-Xms256m -Xmx256m'
          ports:
            - containerPort: 9092
          readinessProbe:
            tcpSocket:
              port: 9092
            initialDelaySeconds: 20
          volumeMounts:
            - name: kafka-data
              mountPath: /var/lib/kafka/data
  volumeClaimTemplates:
    - metadata:
        name: kafka-data
      spec:
        accessModes: [ReadWriteOnce]
        resources:
          requests:
            storage: 2Gi

````

### deploy_script.sh

Применяет StatefulSet-инфраструктуру и Deployment приложения, подставляет тег образа и ждёт готовности deployment/kafka-demo. Контекст задаётся явно.

````text
#!/usr/bin/env sh
set -eu
: "${KUBE_CONTEXT:?Set explicit KUBE_CONTEXT}"
: "${1:?Pass immutable image reference}"
kubectl --context "$KUBE_CONTEXT" apply -f k8s/namespace.yaml
kubectl --context "$KUBE_CONTEXT" apply -f k8s/zookeeper.yaml -f k8s/kafka.yaml
kubectl --context "$KUBE_CONTEXT" -n kafka-homework rollout status statefulset/zookeeper --timeout=300s
kubectl --context "$KUBE_CONTEXT" -n kafka-homework rollout status statefulset/kafka --timeout=600s
# Постоянное приложение разворачивается именно как Deployment.
kubectl --context "$KUBE_CONTEXT" set image --local -f kafka-demo-deployment.yaml \
  "kafka-demo=$1" -o yaml | kubectl --context "$KUBE_CONTEXT" apply -f -
kubectl --context "$KUBE_CONTEXT" -n kafka-homework rollout status deployment/kafka-demo --timeout=180s
kubectl --context "$KUBE_CONTEXT" -n kafka-homework logs deployment/kafka-demo --tail=10

````

### run_checks.ps1

Локальный сценарий: проверка Compose, запуск брокера, сборка, unit/integration, приложение и сохранение логов с проверкой exit code.

````text
# Запускайте из каталога решения в PowerShell с доступом к Docker Desktop.
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
New-Item -ItemType Directory -Force evidence | Out-Null

function Invoke-Checked {
    param([string]$Log, [string]$Program, [string[]]$Arguments)
    # Windows PowerShell 5.1 оформляет stderr native-команд как ErrorRecord;
    # Docker пишет туда и обычный progress. Проверяем фактический exit code.
    $ErrorActionPreference = 'Continue'
    & $Program @Arguments 2>&1 | Tee-Object -FilePath (Join-Path 'evidence' $Log)
    if ($LASTEXITCODE -ne 0) { throw "Команда завершилась с ошибкой: $Program $Arguments" }
}

Invoke-Checked 'compose-config.log' 'docker' @('compose','config','--quiet')
Invoke-Checked 'compose-up.log' 'docker' @('compose','up','-d','--wait','kafka')
Invoke-Checked 'app-build.log' 'docker' @('compose','build','app')
Invoke-Checked 'unit.log' 'docker' @('compose','run','--rm','app','python','-m','pytest','tests/unit','-v')
Invoke-Checked 'integration.log' 'docker' @('compose','run','--rm','app','python','-m','pytest','tests/integration','-v')
Invoke-Checked 'app.log' 'docker' @('compose','run','--rm','app')
Invoke-Checked 'compose-ps.log' 'docker' @('compose','ps')

````

### .dockerignore

Исключает инструменты, журналы, архивы и кэши из Docker build context.

````text
.git
evidence
tools
__pycache__
.pytest_cache
*.md
*.tar

````

### .gitignore

Не позволяет публиковать инструменты, tar-архивы, кэши, виртуальные окружения, .env и kubeconfig.

````text
tools/
*.tar
__pycache__/
.pytest_cache/
*.pyc
.venv*/
.env
*.kubeconfig

````

### README.md

Инструкция, соответствующая обязательной структуре app/requirements.txt и запуску Deployment именно в Docker Desktop Kubernetes.

````text
# Kafka: исправленное решение по пяти пунктам задания

Опубликованный проект: [KuleshovAP/kuber](https://github.com/KuleshovAP/kuber).
Файл для сдачи с исходниками и журналами: [SOLUTION.md](SOLUTION.md).

## Структура

```text
homework_kafka_fixed/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── kafka_client.py
│   └── requirements.txt
├── tests/unit/test_kafka_client.py
├── tests/integration/test_integration.py
├── Dockerfile
├── docker-compose.yml
├── .gitlab-ci.yml
├── .github/workflows/ci.yml
├── kafka-demo-deployment.yaml
├── k8s/namespace.yaml
├── k8s/zookeeper.yaml
├── k8s/kafka.yaml
├── deploy_script.sh
├── run_checks.ps1
├── .dockerignore
├── .gitignore
├── README.md
├── build_report.py
├── repository.json
├── SOLUTION.md
└── evidence/
```

**Список зависимостей расположен именно в `app/requirements.txt`.** В корне
исправленного проекта второго requirements.txt нет. Dockerfile и CI используют
`pip install -r app/requirements.txt`.

## 1. Kafka и ZooKeeper через Docker Compose

Нужны Windows x64 и запущенный Docker Desktop в режиме Linux containers.
Добавьте Docker CLI и kubectl в PATH, если команды не найдены:

```powershell
$env:PATH = "$env:LOCALAPPDATA\Programs\DockerDesktop\resources\bin;" + $env:PATH
docker compose up -d --wait kafka
docker compose ps
```

Kafka доступна с хоста по `localhost:9092`, из контейнеров — по `kafka:29092`.
ZooKeeper использует порт 2181 внутри сети Compose. Данные сохраняются в
named volumes. Healthcheck проверяет реальный запрос списка topic.

## 2–3. Приложение, образ, сообщение и тесты

```powershell
docker compose build app
docker compose run --rm app
docker compose run --rm app python -m pytest tests/unit tests/integration -v
```

Приложение создаёт уникальный topic, отправляет JSON, получает его обратно,
проверяет совпадение и печатает topic/partition/offset/received. Тестовый topic
удаляется после проверки. Ожидания ограничены тайм-аутами; старое сообщение
не может привести к ложному успеху. Producer использует `acks=all`.

Однократный запуск — режим по умолчанию для Compose. Для Kubernetes Deployment
предусмотрен `--continuous`: обмен повторяется каждые 30 секунд. После первого
успешного обмена создаётся `/tmp/kafka-demo-ready`; readinessProbe проверяет
этот файл. Приложение остаётся работающим, а не завершается как Job.

## 4. Публикация всего проекта и CI/CD

Проект должен находиться в настоящем репозитории GitHub либо GitLab.
Локальный ZIP, подготовленный YAML или локальный `git init` не заменяют
публикацию. Факт публикации подтверждается действительной ссылкой и commit SHA
в итоговом SOLUTION.md; если их нет, этот пункт ещё не завершён.

В GitHub используется `.github/workflows/ci.yml`: unit, сборка приложения,
запуск реальной Kafka, integration-тест и сохранение лога. В GitLab используется
`.gitlab-ci.yml`: test → build → manual deploy. Для Docker-in-Docker необходим
изолированный privileged runner. Учётные данные registry берутся из переменных
GitLab, пароль передаётся через stdin. Удалённое выполнение pipeline не
подменяется заявлением о локальных тестах.

`deploy_script.sh` применяет инфраструктуру Kafka и **Deployment приложения**,
подставляет переданный тег образа, ждёт rollout и выводит логи. Для него нужны
явный `KUBE_CONTEXT`, kubeconfig и доступ к указанному образу. Hosted runner
сам по себе не получает доступ к локальному Docker Desktop пользователя.

## 5. Kubernetes именно в Docker Desktop

Откройте **Docker Desktop → Kubernetes → Create cluster → Create**. Дождитесь
готовности кластера. В современных версиях Desktop доступны два встроенных
provisioner: kubeadm и kind. Оба относятся к Kubernetes **самого Docker Desktop**;
это описано в [официальной документации](https://docs.docker.com/desktop/use-desktop/kubernetes/).
Отдельная команда `kind create cluster` в этом решении не применяется.

Проверьте именно контекст `docker-desktop`:

```powershell
docker desktop kubernetes status
kubectl --context docker-desktop cluster-info
kubectl --context docker-desktop get nodes
```

Подготовьте образ с фиксированным тегом и примените манифесты:

```powershell
docker tag kafka-homework-app:local kafka-homework-app:desktop
kubectl --context docker-desktop apply -f k8s/namespace.yaml
kubectl --context docker-desktop apply -f k8s/zookeeper.yaml -f k8s/kafka.yaml
kubectl --context docker-desktop -n kafka-homework rollout status statefulset/zookeeper --timeout=300s
kubectl --context docker-desktop -n kafka-homework rollout status statefulset/kafka --timeout=600s
kubectl --context docker-desktop apply -f kafka-demo-deployment.yaml
kubectl --context docker-desktop -n kafka-homework rollout status deployment/kafka-demo --timeout=180s
kubectl --context docker-desktop -n kafka-homework get deployments,pods,pvc
kubectl --context docker-desktop -n kafka-homework logs deployment/kafka-demo --tail=10
```

`kafka-demo-deployment.yaml` находится в корне и содержит `kind: Deployment`,
одну реплику и постоянный процесс приложения. Kafka и ZooKeeper используют
StatefulSet и PVC: это инфраструктура, а не замена Deployment приложения.
Три брокера находятся на одном узле, поэтому пример не защищён от отказа узла.
ZooKeeper также одиночный. PLAINTEXT предназначен для учебной локальной сети.

Чтобы освободить память перед Kubernetes, можно остановить только учебные
Compose-сервисы: `docker compose stop kafka zookeeper`. Удалять тома не нужно.

Результаты текущей проверки приведены в SOLUTION.md и evidence. Прежние логи
контекста `kind-kafka-homework` не используются как доказательство работы
Docker Desktop Kubernetes.

````

### build_report.py

Генерирует этот самодостаточный Markdown с полным исходным кодом, ссылкой на публикацию при её наличии и реальными журналами текущей версии.

````text
"""Собирает отчёт по пяти требованиям из исходников и журналов этой версии."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FILES = {
    'app/requirements.txt': 'Обязательный список зависимостей внутри app: kafka-python и pytest. Именно этот путь используется Dockerfile и обоими вариантами CI.',
    'app/__init__.py': 'Объявляет Python-пакет app.',
    'app/kafka_client.py': 'Создаёт уникальный topic, отправляет UTF-8 JSON с acks=all, читает с earliest с тайм-аутом и сверяет событие. В finally закрывает клиентов и удаляет временный topic. Replication factor берётся из окружения: 1 в Compose, 3 в Kubernetes.',
    'app/main.py': 'Точка входа. По умолчанию выполняет один обмен; --continuous оставляет приложение работающим и повторяет обмен. Readiness-маркер появляется после успешного получения сообщения.',
    'Dockerfile': 'Корневой Dockerfile Python 3.11.11: копирует app/requirements.txt, устанавливает зависимости именно из него, затем копирует app и tests. Запускает python -m app.main.',
    'docker-compose.yml': 'Kafka 7.9.0 и ZooKeeper 7.9.0, постоянные тома, внутренний/внешний listeners и healthcheck Kafka. app запускается после готовности брокера. Provenance отключён для совместимости локального импорта образа.',
    'tests/unit/test_kafka_client.py': 'Проверяет сохранение Unicode и чисел при сериализации без брокера.',
    'tests/integration/test_integration.py': 'Проверяет настоящий обмен с Kafka, текст, значение, partition и offset уникального topic.',
    '.gitlab-ci.yml': 'GitLab pipeline со стадиями test/build/deploy: unit и integration, сборка/push по commit SHA, ручной deploy через deploy_script.sh.',
    '.github/workflows/ci.yml': 'Рабочая конфигурация GitHub Actions для push/PR/manual: unit и integration с реальной Kafka, сборка Docker-образа и сохранение диагностики.',
    'kafka-demo-deployment.yaml': 'Обязательный корневой манифест приложения: apps/v1 Deployment kafka-demo, одна реплика, постоянный процесс --continuous, readinessProbe после обмена с Kafka и ограничения ресурсов. Это не Job.',
    'k8s/namespace.yaml': 'Отдельный namespace kafka-homework в выбранном контексте docker-desktop.',
    'k8s/zookeeper.yaml': 'Headless Service и StatefulSet одиночного ZooKeeper с PVC 1 Gi и проверкой доступности TCP.',
    'k8s/kafka.yaml': 'Bootstrap Service, headless Service и StatefulSet трёх брокеров с PVC по 2 Gi. broker.id — числовой ordinal, advertised listener — DNS своего Pod. enableServiceLinks=false устраняет конфликт KAFKA_PORT.',
    'deploy_script.sh': 'Применяет StatefulSet-инфраструктуру и Deployment приложения, подставляет тег образа и ждёт готовности deployment/kafka-demo. Контекст задаётся явно.',
    'run_checks.ps1': 'Локальный сценарий: проверка Compose, запуск брокера, сборка, unit/integration, приложение и сохранение логов с проверкой exit code.',
    '.dockerignore': 'Исключает инструменты, журналы, архивы и кэши из Docker build context.',
    '.gitignore': 'Не позволяет публиковать инструменты, tar-архивы, кэши, виртуальные окружения, .env и kubeconfig.',
    'README.md': 'Инструкция, соответствующая обязательной структуре app/requirements.txt и запуску Deployment именно в Docker Desktop Kubernetes.',
    'build_report.py': 'Генерирует этот самодостаточный Markdown с полным исходным кодом, ссылкой на публикацию при её наличии и реальными журналами текущей версии.',
    'repository.json': 'Адрес предоставленного пользователем репозитория и проверенный статус публикации. published=true выставляется только после успешного push и проверки удалённого commit.',
}


def main():
    result = ['# Kafka, CI/CD и Kubernetes — исправленная версия\n\n',
              'Автор: Кулешов Алексей Петрович.\n\n',
              '## Исправления по замечаниям\n\n',
              '1. Зависимости находятся в **app/requirements.txt**, корневого requirements.txt в этой поставке нет. Dockerfile и CI обновлены.\n',
              '2. Подготовлены CI-файлы для GitHub и GitLab. Наличие настоящего репозитория подтверждается только ссылкой и commit ниже.\n',
              '3. Добавлен **kafka-demo-deployment.yaml** с **kind: Deployment**. Приложение имеет постоянный режим и readiness после реального обмена.\n',
              '4. Требуемая среда — Kubernetes, включённый в интерфейсе **Docker Desktop**, контекст **docker-desktop**. Прежний отдельный kind-кластер не считается подтверждением этого пункта.\n\n']
    publication = ROOT / 'repository.json'
    data = json.loads(publication.read_text(encoding='utf-8')) if publication.exists() else {}
    if data.get('published') and data.get('commit'):
        result += [f'## Репозиторий\n\n[Проект]({data["url"]})\n\nCommit с проверенными исходниками: `{data["commit"]}`. Отчёт дополняется отдельными документационными commit.\n\n']
        if data.get('ci_url'):
            result += [f'GitHub Actions: [подтверждённый запуск]({data["ci_url"]}), результат **{data["ci_conclusion"]}**.\n\n']
    else:
        result += ['## Публикация: обязательный пункт ещё не завершён\n\n',
                   f'Целевой репозиторий: {data.get("url", "не указан")}. Для push ожидается авторизация с правом записи. ZIP или локальный Git не выдаются за выполненную публикацию. До публикации комплект не следует считать полностью готовым к пересдаче.\n\n']
    result += ['## Подтверждение запуска\n\n',
               'Только журналы **этой версии** ниже подтверждают выполненные проверки. Включение настройки без Ready Deployment не считается успешным запуском приложения.\n\n']
    for path in sorted((ROOT / 'evidence').glob('*')):
        raw = path.read_bytes()
        encoding = 'utf-16' if raw.startswith(b'\xff\xfe') else 'utf-8-sig'
        text = raw.decode(encoding, errors='replace')
        if len(text) > 12000:
            lines = text.splitlines()
            text = '\n'.join(lines[:12] + ['... середина журнала опущена; полный файл приложен ...'] + lines[-55:])
        result += [f'### evidence/{path.name}\n\n````text\n{text}\n````\n\n']
    result += ['## Назначение и полное содержимое файлов\n\n']
    for relative, description in FILES.items():
        path = ROOT / relative
        text = path.read_text(encoding='utf-8')
        result += [f'### {relative}\n\n{description}\n\n````text\n{text}\n````\n\n']
    result += ['## Источник по Docker Desktop Kubernetes\n\n',
               '[Официальная документация Docker](https://docs.docker.com/desktop/use-desktop/kubernetes/) описывает оба встроенных provisioner (kubeadm/kind) и контекст docker-desktop. Управляемый кластер Docker Desktop отличается от отдельного kind create cluster.\n']
    (ROOT / 'SOLUTION.md').write_text(''.join(result), encoding='utf-8')
    print('Created corrected SOLUTION.md')


if __name__ == '__main__':
    main()

````

### repository.json

Адрес предоставленного пользователем репозитория и проверенный статус публикации. published=true выставляется только после успешного push и проверки удалённого commit.

````text
{
  "url": "https://github.com/KuleshovAP/kuber",
  "published": true,
  "commit": "16ada2876f3f4c704af35281e4f0e8eee110a5e0",
  "ci_url": "https://github.com/KuleshovAP/kuber/actions/runs/42649184940",
  "ci_conclusion": "success"
}

````

## Источник по Docker Desktop Kubernetes

[Официальная документация Docker](https://docs.docker.com/desktop/use-desktop/kubernetes/) описывает оба встроенных provisioner (kubeadm/kind) и контекст docker-desktop. Управляемый кластер Docker Desktop отличается от отдельного kind create cluster.
