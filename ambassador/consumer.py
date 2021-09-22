from confluent_kafka import Consumer
import json, os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

import core.listeners
from core.models import KafkaError

consumer = Consumer({
    'bootstrap.servers': os.getenv('BOOTSTRAP_SERVERS'),
    'security.protocol': os.getenv('SECURITY_PROTOCOL'),
    'sasl.username': os.getenv('SASL_USERNAME'),
    'sasl.password': os.getenv('SASL_PASSWORD'),
    'sasl.mechanism': os.getenv('SASL_MECHANISMS'),
    'group.id': os.getenv('GROUP_ID'),
    'auto.offset.reset': 'earliest'
})

consumer.subscribe([os.getenv('KAFKA_TOPIC')])

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    print(msg.key())

    try:
        getattr(core.listeners, msg.key().decode('utf-8'))(json.loads(msg.value()))
    except Exception as e:
        print(e)

        KafkaError.objects.create(
            key=msg.key(),
            value=msg.value(),
            error=e,
        )

consumer.close()
