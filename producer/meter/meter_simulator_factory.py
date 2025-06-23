from enum import Enum
from meter.residential_meter_simulator import ResidentialMeterSimulator

class MeterType(Enum):
    RESIDENTIAL = 'residential'


class MeterSimulatorFactory():
    def __init__(self) -> None:
        pass

    def create_producer(self, input_type: str, _id: int, _config: dict):
        if input_type in MeterType.__members__:
            if input_type == 'RESIDENTIAL':
                return ResidentialMeterSimulator(_id, _config)
        else:
            return None
            
              

