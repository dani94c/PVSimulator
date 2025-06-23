# Mimics actual household consumption patterns generating random, but continues, values (values change smoothly over time). 
# By default, generated values should be from 0.0 to 10.0 kW

import random
from meter.meter_simulator import MeterSimulator

class ResidentialMeterSimulator(MeterSimulator):
    def __init__(self, _id: int, _config: dict):
        super().__init__(_id)

        # Base consumption always present in a household. This represents appliances that run continuously
        # Default start at 1kW (reasonable baseline for house power consumption is in range 0.5-1.5 kW)
        self.baseline_power = _config.get("baseline", 1.0)      #kW
        
        # Variable consumption - This represents the dynamic part that turn on and off throughout the day
        self.variable_power = random.uniform(0.5, 3.0)      # kW

        #Set lower bound for energy consumption generated values. Default is 0.0 kW
        self.min_power = _config.get("min_power", 0.0)      #kW

        #Set upper bound for energy consumption generated values. Default is 10.0 kW
        self.max_power = _config.get("max_power", 10.0)      #kW

        print(f'Baseline: {self.baseline_power}, vp: {self.variable_power}, min: {self.min_power}, max: {self.max_power}')

        
    def get_next_reading(self):
        # Calculate small random change only for the variable consumption (±10% of variable value, max ±0.5kW). 
        # This creates realistic gradual changes rather than sudden spikes
        max_change = min(0.5, self.variable_power * 0.1)
        change = random.uniform(-max_change, max_change)
        
        # The variable part can drop to 0 (all variable appliances off) but not below
        # Upper limit is calculated to ensure total never exceeds max_power kW when added to baseline
        self.variable_power = max(0.0, min((self.max_power - self.baseline_power), self.variable_power + change))
        
        # Total consumption is obtained from baseline (always on) plus variable (dynamic) components
        total_power = self.baseline_power + self.variable_power

        # Additional check to ensure to stay within the specified kW range
        total_power = max(self.min_power, min(self.max_power, total_power))

        return round(total_power, 2)