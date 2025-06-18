import pika, time


try:
    #time.sleep(10)
    print("Starting connection...")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq-host', port=5672))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    print("Connected! Listening for messages...")

    def callback(ch, method, properties, body):
        print(f"Received {body}")

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
except KeyboardInterrupt:
    print("Closing...")
    exit(0)