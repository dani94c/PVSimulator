import pika, time
import signal

def shutdown_handler(signum, frame):
    print("\nSginal received. Closing...")
    try:
        channel.stop_consuming()
    except Exception:
        pass

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)


try:
    #time.sleep(10)
    print("Starting connection...")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq-host', port=5672))
    channel = connection.channel()

    channel.queue_declare(queue='home_power_data')

    print("Connected! Listening for messages...")

    def callback(ch, method, properties, body):
        print(f"Received {body}")

    channel.basic_consume(queue='home_power_data', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
finally:
    if channel.is_open:
        channel.close()
    if connection.is_open:
        connection.close()
    print("PV SIMULATOR || All connections are closed")
    exit(0)