from confluent_kafka import Consumer, KafkaError

# Define Kafka consumer configuration
consumer_config = {
    'bootstrap.servers': '127.0.0.1:19092',  # Replace with your Kafka bootstrap servers and port
    'group.id': 'testing-kafka',  # Specify a consumer group ID
    'auto.offset.reset': 'earliest',
}

# Create Kafka consumer instance
consumer = Consumer(consumer_config)

# Subscribe to the Kafka topic
topic = 'testing-kafka'
consumer.subscribe([topic])

try:
    while True:
        # Poll for messages
        msg = consumer.poll(1.0)  # Adjust the timeout as needed

        if msg is None:
            continue
        if msg.error():
            # Handle Kafka errors
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event, not an error
                continue
            else:
                print(f"Error: {msg.error()}")
                break

        # Process the received message
        key = msg.key().decode('utf-8') if msg.key() else None
        value = msg.value().decode('utf-8') if msg.value() else None
        print(f"Received message - Key: {key}, Value: {value}")

except KeyboardInterrupt:
    pass
finally:
    # Close down consumer to commit final offsets
    consumer.close()
