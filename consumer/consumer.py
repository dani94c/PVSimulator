import signal
from pv_simulator import PVSimulator
from config import pv_config
import sys

#time.sleep(10)


def shutdown_handler(signum, frame):
    print("\nSginal received. Closing...")
    try:
        simulator.stop_simulator()
    except Exception:
        pass

signal.signal(signal.SIGINT, shutdown_handler)

#Handling uncaught exception
def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
    # Logs lo stack trace
    print(f"Uncaught exception:, {exc_type}, {exc_value}, {exc_traceback}")

sys.excepthook = handle_uncaught_exception



try:
    print(f'STARTING PV SIMULATOR...')
    _pv_config = pv_config
    simulator = PVSimulator(_pv_config)
    simulator.run()

except Exception as e:
    print(e)

finally:
    exit(1)