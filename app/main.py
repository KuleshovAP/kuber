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
