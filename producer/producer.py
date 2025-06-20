import pika
from datetime import datetime
import time
import random
import json
import signal
import sys


#Handle clean clousure of active connection to rabbitmq broker
def shutdown_handler(sig, frame):
    print("\nSignal received, closing connections...")
    if channel.is_open:
        channel.close()
    if connection.is_open:
        connection.close()
    print("Connection closed.")
    sys.exit(0)

# Register handler for received signals 
signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

#Handling uncaught exception
def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
    # Logs lo stack trace
    print(f"Uncaught exception:, {exc_type}, {exc_value}, {exc_traceback}")

sys.excepthook = handle_uncaught_exception

# Mimics actual household consumption patterns generating random, but continues, values (values change smoothly over time). 
# They can assume values from 0.0 to 10.0 kW
class MeterSimulator:
    def __init__(self):
        self.current_power = 1.0      #Start at 1kW (reasonable baseline for house power conumptions)
        
    def get_next_reading(self):
        # Small random change (±10% of current value, max ±0.5kW)
        max_change = min(0.5, self.current_power * 0.1)
        change = random.uniform(-max_change, max_change)
        
        self.current_power = max(0.0, min(10.0, self.current_power + change))  #Meter must generates values between 0.0 and 10.0 kW
        return round(self.current_power, 2)



#time.sleep(10)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq-host', port=5672))
channel = connection.channel()

# Specify pv_id to which send data in the queue name. 
# Usefull if in a simulation it's required to emulate more PVs
channel.queue_declare(queue='home_power_data_pv0')

#msg = f"{datetime.now().strftime("%d/%m/%Y, %H:%M:%S")} Hello World!"

# for i in range(0,5):
#     channel.basic_publish(exchange='', routing_key='hello', body=f"[{datetime.now().strftime("%d/%m/%YT%H:%M:%S")}] Hello World!")
#     print(f"[{i}] Sent Hello World")
#     time.sleep(3)

meter = MeterSimulator()

while True:
    power_reading = meter.get_next_reading()
    sampling_timestamp = datetime.now().isoformat()

    print(f'{sampling_timestamp} || METER SIMULATOR || New power consumption generated: {power_reading} kW')
    
    message = {
        "meter_id": "0",
        "timestamp": sampling_timestamp,
        "meter_power_kw": power_reading,
        "type": "house_meter_reading"
    }
    
    try:
        channel.basic_publish(
            exchange='',
            routing_key='home_power_data_pv0',  
            body=json.dumps(message)
        )
        print(f'Published meter power value: {power_reading} kW')
    except Exception as e:
        print(f'Failed to publish message: {e}')

    
    time.sleep(2)  # Produce meter reading every 2 seconds