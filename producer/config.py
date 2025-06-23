meter_config = {
    "id" : 0,
    "pv_id" : "pv0",
    "meter_type" : "RESIDENTIAL",       # Specifies the type of building whose energy consumption is to be simulated
    "baseline" : 1.2,                   # Power consumption always present in a real building (house in this case). Typical baseline for residential is 0.5-1.5 kW
    "min_power" : 0.0,                  # Lower bound (in kW) for meter values (power consumption) generation in the simulation
    "max_power" : 10.0,                 # Upper bound (in kW) for meter values (power consumption) generation in the simulation
    "meter_interval_sec" : 2            # Specifies how often new power consumption data should be generated
}