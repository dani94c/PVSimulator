"""
PV Simulator - Generates photovoltaic power production values and processes data
"""

import pika
import json
import math
from time import time
import os
import csv
from datetime import datetime
from collections import deque


class PVSimulator:
    def __init__(self, _id):
        self.pv_id = _id
        self.connection = None
        self.channel = None
        self.queue_name = f'home_power_data_pv{self.pv_id}'
        self.data_dir = '/pv_simulator/data'
        self.pv_dir = os.path.join(self.data_dir, f'PV{self.pv_id}')
        self.output_file = os.path.join(self.pv_dir, f'energy_data_{int(time())}.csv')

        print(self.pv_dir)
        
        # Buffer to store recent meter readings
        self.meter_readings = deque(maxlen=1)
        
        # Ensure data directory exists
        os.makedirs(self.pv_dir, exist_ok=True)
        
        # Initialize CSV file with headers
        self.init_csv_file()
        
    def init_csv_file(self):
        """Initialize CSV file with headers"""
        try:
            with open(self.output_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['timestamp', 'meter_power_kw', 'pv_power_kw', 'net_power_kw'])
                print(f"Initialized CSV file: {self.output_file}")
        except Exception as e:
            print(e)
    
    def connect_to_rabbitmq(self):
        """Establish connection to RabbitMQ"""
        try:
            print("Starting connection...")
            if self.connection == None:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq-host', port=5672))
                if self.channel == None:
                    self.channel = self.connection.channel()
                    self.channel.queue_declare(queue=self.queue_name)

            print("Connected! Listening for messages...")

            return True
                
        except Exception as e:
            print(f"Failed to connect to RabbitMQ: {e}")
            return False
    
   
    def start_consuming(self):
        """Start consuming messages from RabbitMQ"""
        try:
            self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.process_meter_reading, auto_ack=True)
            
            print("PV Simulator waiting for meter readings... To exit press CTRL+C'")
            self.channel.start_consuming()
            
        except KeyboardInterrupt:
            print("Stopping PV Simulator...")
            self.channel.stop_consuming()
        except Exception as e:
            print(f"Error in consuming: {e}")


    def generate_pv_power(self):
        """Generate PV power based on solar curve (similar to a gaussian curve)"""
        current_time = datetime.now()
        hour = current_time.hour
        minute = current_time.minute
        
        # Convert to decimal hours (0-24)
        decimal_hour = hour + minute / 60.0
        
        # Solar power generation follows a bell curve
        # In a standard day:
        # Peak at solar noon (around 12:00)
        # No generation from 19:00 to 6:00 (night)
        
        if decimal_hour < 6 or decimal_hour > 19:
            # Night time - no solar generation
            return 0.0
        
        # Daylight hours - bell curve centered at 12:30
        peak_hour = 12.5
        max_power = 8.0  # Maximum PV power in kW (value for a medium domestic photovoltaic system)
        
        # Gaussian curve formula: max_power * exp(-((hour - peak_hour)^2) / (2 * sigma^2))
        sigma = 3.5  # Controls the width of the gaussian curve, so after how many hours from the peak, the generated power decreases significantly
        power = max_power * math.exp(-((decimal_hour - peak_hour) ** 2) / (2 * sigma ** 2))
        
        # Add some randomness to simulate weather conditions
        weather_factor = max(0.3, min(1.2, 1.0 + (hash(str(current_time.minute)) % 100 - 50) / 200))
        power *= weather_factor

        #print(f'PV{self.pv_id} generated value {power} at time: {current_time}')
        
        return round(max(0, power), 2)
    
    def process_meter_reading(self, ch, method, properties, body):
        """Process incoming meter readings"""
        try:
            message = json.loads(body)
            meter_id = message.get('meter_id')
            meter_value = message.get('meter_power_kw',0) #retrieve meter from payload, otherwise set to 0
            timestamp = message.get('timestamp')
            
            # Store the latest meter reading
            self.meter_readings.append({
                'meter_id': meter_id,
                'timestamp': timestamp,
                'meter_value': meter_value
            })

            timestamp_str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            print(f"{timestamp_str} || PV SIMULATOR {self.pv_id} || Received meter reading from meter {meter_id}: {meter_value} kW")
            
            # Generate PV power
            pv_power = self.generate_pv_power()
            
            # Calculate net power (PV generation - meter consumption) rounded to the second decimal digit
            net_power = round(pv_power - meter_value, 2)

            print(f'pv_timestamp: {timestamp_str}, meter_timestamp: {timestamp}, meter_id: {meter_id}, meter_value: {meter_value} kW, pv_power: {pv_power} kW, net_power: {net_power} kW')
            
            # Write to CSV file
            self.write_to_csv(timestamp, meter_value, pv_power, net_power)
            
            #print(f"PV: {pv_power} kW, Meter: {meter_value} kW, Net: {net_power} kW")
            
            
        except Exception as e:
            print(f"Error processing meter reading: {e}")
    
    def write_to_csv(self, timestamp, meter_power, pv_power, net_power):
        """Write data to CSV file"""
        try:
            with open(self.output_file, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([timestamp, meter_power, pv_power, net_power])
        except Exception as e:
            print(f"Failed to write to CSV: {e}")

    def stop_simulator(self):
        print("Stopping PV Simulator...")
        self.channel.stop_consuming()

        if self.channel.is_open():
            self.channel.close()

        if self.connection and not self.connection.is_closed:
            self.connection.close()
            print("Connection closed")

    
    def run(self):
        """Main simulation loop"""
        print("Starting PV Simulator...")
        
        if not self.connect_to_rabbitmq():
            return
        
        try:
            self.start_consuming()
        finally:
            if self.connection and not self.connection.is_closed:
                self.connection.close()
                print("Connection closed")

