from confluent_kafka import Consumer, KafkaException, KafkaError
import json

# Configure the consumer
consumer = Consumer({
    'bootstrap.servers': 'kafka:29092,',
    'group.id': 'stock-price-group',
    'auto.offset.reset': 'earliest'  # Start from the earliest message if no offset is committed
})

# Subscribe to the relevant topics
topics = ['stock_ticks31']
consumer.subscribe(topics)


try:
    while True:
        # Poll for messages with a 1-second timeout
        msg = consumer.poll(1.0)
        
        # Skip if no message is received
        if msg is None:
            continue
        
        # Handle errors
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue
        
        # Deserialize JSON message
        data = json.loads(msg.value().decode('utf-8'))
        
        # Print message with topic information
        print(f"Received from {msg.topic()}: {data}")

except KeyboardInterrupt:
    print("Stopping consumer")
finally:
    # Close consumer to release resources
    consumer.close()
