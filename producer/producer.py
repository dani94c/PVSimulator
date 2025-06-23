import pika
from datetime import datetime
import time
import json
import signal
import sys
from meter.meter_simulator_factory import MeterSimulatorFactory
from meter.meter_simulator import MeterSimulator
import logging
from config import meter_config

#Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s || %(levelname)s || METER-SIMULATOR || %(message)s')
logger = logging.getLogger(__name__)


#Handle clean clousure of active connection to rabbitmq broker
def shutdown_handler(sig, frame):
    print("\nSignal received, closing connections...")
    if channel.is_open:
        channel.close()
    if connection.is_open:
        connection.close()
    print("Connection closed.")
    exit(0)

# Register handler for received signals 
signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

#Handling uncaught exception
def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
    # Logs lo stack trace
    print(f"Uncaught exception:, {exc_type}, {exc_value}, {exc_traceback}")

sys.excepthook = handle_uncaught_exception



#Create producer factory
msf = MeterSimulatorFactory()
meter_id = meter_config.get("id",0)     #Default id is 0

meter_type = meter_config.get("meter_type", "RESIDENTIAL")      #Default type is RESIDENTIAL

#Create required meter simulator
meter: MeterSimulator = msf.create_producer(meter_type, meter_id, meter_config)
if(meter == None):
    logger.error("The specified type of meter is not supported in the simulator. Exit the simulation")
    exit(0)


# Setup communication through RabbitMQ
try: 
    #time.sleep(10)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq-host', port=5672))
    channel = connection.channel()

    # Specify pv_id to which send data in the queue name. 
    # Usefull in a possible future simulator extension, if in a simulation it's required to emulate more PVs and it could be necessary
    # to specify a specific queue to which send data
    pv_id = meter_config.get("pv_id","pv0")     #Default use "pv0" as pv_id
    queue_name = f'home_power_data_{pv_id}'
    channel.queue_declare(queue=queue_name)

except Exception as e:
    print(e)


#Start simulation
while True:
    power_reading = meter.get_next_reading()
    sampling_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    logging.info(f'New power consumption generated at {sampling_timestamp} : {power_reading} kW')
    
    message = {
        "meter_id": meter.id,
        "timestamp": sampling_timestamp,
        "meter_power_kw": power_reading,
        "type": f"{meter_type.lower()}_meter_reading"
    }
    
    logging.info(f'Sending message: {message}')
    try:
        # Use default exchange, type direct
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,  
            body=json.dumps(message)
        )
        logging.info(f'Published meter power value: {power_reading} kW')
    except Exception as e:
        logging.error(f'Failed to publish message: {e}')

    
    time.sleep(meter_config["meter_interval_sec"])  # Produce meter reading every 2 seconds