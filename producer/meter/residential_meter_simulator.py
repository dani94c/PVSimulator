# Mimics actual household consumption patterns generating random, but continues, values (values change smoothly over time). 
# They can assume values from 0.0 to 10.0 kW

import random
from meter.meter_simulator import MeterSimulator

class ResidentialMeterSimulator(MeterSimulator):
    def __init__(self, _id: int):
        super().__init__(_id)
        self.baseline_power = 1.0      #Start at 1kW (reasonable baseline for house power conumptions)
        self.current_power = self.baseline_power
        
    def get_next_reading(self):
        # Small random change (±10% of current value, max ±0.5kW)
        max_change = min(0.5, self.current_power * 0.1)
        change = random.uniform(-max_change, max_change)
        
        self.current_power = max(0.0, min(10.0, self.current_power + change))  #Meter must generates values between 0.0 and 10.0 kW
        return round(self.current_power, 2)