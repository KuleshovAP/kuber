import json
from app.kafka_client import encode_event


def test_event_preserves_unicode_and_numbers():
    event = {'message': 'Привет, Kafka!', 'value': 42}
    encoded = encode_event(event)
    assert isinstance(encoded, bytes)
    assert json.loads(encoded.decode('utf-8')) == event
