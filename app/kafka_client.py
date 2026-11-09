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
