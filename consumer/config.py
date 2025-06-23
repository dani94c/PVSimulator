pv_config = {
    "id" : 0,
    "power_gen_start" : 6.0,  # When the pv starts to produce power in the morning, in decimal (kW = 0.0 before this time)
    "power_gen_stop" : 19.0,  # When the pv stops to produce power in the evening, in decimal (kW = 0.0 after this time)
    "peak_hour" : 12.5,       # Peak of solar power generation, in decimal - Bell curve centered at this value
    "max_power" : 8.0,        # Maximum PV power in kW (8 should be a reasonable value for a medium domestic photovoltaic system)
    "sigma" : 3.5             # Controls the width of the gaussian curve, so after how many hours from the peak, the generated power decreases significantly
}