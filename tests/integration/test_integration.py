from app.kafka_client import roundtrip


def test_real_broker_roundtrip():
    result = roundtrip()
    assert result['received']['message'] == 'Hello, Kafka!'
    assert result['received']['value'] == 42
    assert result['partition'] == 0
    assert result['offset'] == 0
