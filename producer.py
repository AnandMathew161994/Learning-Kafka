from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
import asyncio, json, random, time


admin_client = AdminClient({'bootstrap.servers':'localhost:19092,localhost:19094,localhost:19095'})
TOPICS = ['stock_ticks31']

def ensure_topics_exist():
    existing_topics = admin_client.list_topics(timeout=5).topics

    new_topics = [
        NewTopic(topic, num_partitions=4 ,replication_factor=2)
        for topic in TOPICS if topic not in existing_topics
    ]

    if new_topics:
        print(f"Creating topics: {[t.topic for t in new_topics]}")
        fs = admin_client.create_topics(new_topics)
        for topic, f in fs.items():
            try:
                f.result()
                print(f" Created topic: {topic}")
            except Exception as e:
                print(f"Failed to create topic {topic}: {e}")
    else:
        print("Topics already exist.")



producer = Producer({'bootstrap.servers':'localhost:19092,localhost:19094,localhost:19095'})
symbols = ["AAPL", "TSLA", "GOOG","BERK","LUCID","MFST","ASD","SAD"]  # 1000+ symbols

symbol_prices = {sym: round(random.uniform(100, 500), 2) for sym in symbols}

def update_price(symbol):
    last_price = symbol_prices[symbol]
    # Small random walk — adjust percentage for volatility
    change_pct = random.uniform(-0.5, 0.5) / 100  # +/- 0.5%
    new_price = last_price * (1 + change_pct)
    new_price = round(new_price, 2)
    symbol_prices[symbol] = new_price
    return new_price


async def send_batch():
    for _ in range(100):
        symbol = random.choice(symbols)
        price = update_price(symbol)
        event = {
            "symbol": symbol,
            "price": price,
            "volume": random.randint(10, 1000),
            "timestamp": int(time.time() * 1000)
        }
        for topic in TOPICS:
            producer.produce(topic, key=symbol, value=json.dumps(event))
        
    producer.flush()

async def main():
    ensure_topics_exist()
    while True:
        await send_batch()
        await asyncio.sleep(0.6)  # fine-tune to hit ~16K/sec

asyncio.run(main())
