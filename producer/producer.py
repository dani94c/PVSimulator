import pika
from datetime import datetime
import time

#time.sleep(10)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq-host', port=5672))
channel = connection.channel()

channel.queue_declare(queue='hello')

#msg = f"{datetime.now().strftime("%d/%m/%Y, %H:%M:%S")} Hello World!"

for i in range(0,5):
    channel.basic_publish(exchange='', routing_key='hello', body=f"[{datetime.now().strftime("%d/%m/%YT%H:%M:%S")}] Hello World!")
    print(f"[{i}] Sent Hello World")
    time.sleep(3)

connection.close()
