import signal
from pv_simulator import PVSimulator

#time.sleep(10)


def shutdown_handler(signum, frame):
    print("\nSginal received. Closing...")
    try:
        simulator.stop_simulator()
    except Exception:
        pass

signal.signal(signal.SIGINT, shutdown_handler)



try:
    print(f'STARTING PV SIMULATOR...')
    simulator = PVSimulator("0")
    simulator.run()

except Exception as e:
    print(e)

finally:
    exit(0)