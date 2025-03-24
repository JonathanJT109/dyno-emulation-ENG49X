"""
Testing the PID Loop on the kart using PyVESC.
"""

from multiprocessing import Process
from time import sleep

from pyvesc import VESC
from pyvesc.VESC.VESC import GetValues

from kart.tools import choose_port

from .pid import PIDController

LAPS = 10
MAX_VOLTAGE = 5.0
MIN_VOLTAGE = 0.0
DIAMETER = 0.254  # TODO: Find diameter
KART_RESPONSE_RATE = 0.001
curr = 0
max_rpm = 5000
send_voltage: float = 0
seg_length: float = 10000


def read(kart_port):
    global curr
    while True:
        m = kart_port.get_measurements()
        if isinstance(m, GetValues):
            curr = m.rpm
            print("RPM:", curr)


def main(port, target_rpm: float):
    global curr
    global max_rpm

    # Setting up the PID loop
    # NOTE: Find better coefficients
    kp = 0.01  # Proportional gain
    ki = 0.005  # Integral gain
    kd = 0.002  # Derivative gain
    min_voltage = 0.0  # Minimum voltage output
    max_voltage = 5.0  # Maximum voltage output

    pid = PIDController(
        kp, ki, kd, min_voltage, max_voltage, max_rpm, KART_RESPONSE_RATE
    )

    voltage = 0.0

    print("Step\tRPM Setpoint\tCurrent RPM\tVoltage")
    print("-" * 60)

    loop_i = 0
    with VESC(serial_port=port) as kart:
        while seg_length > 0:
            voltage = pid.compute(target_rpm, curr)

            # TODO: Send voltage to controller
            kart.set_current(1)

            if loop_i == 0:
                print(f"{loop_i}\t{target_rpm:.1f}\t\t{curr:.1f}\t\t{voltage:.2f}")
            loop_i = (loop_i + 1) % 10
            sleep(KART_RESPONSE_RATE)


if __name__ == "__main__":
    try:
        port = choose_port()

        with VESC(serial_port=port) as kart:
            k = Process(
                target=main,
                args=(
                    kart,
                    3000,
                ),
            )
            r = Process(target=read, args=(kart,))
            k.start()
            r.start()
            k.join()
            r.join()
    except KeyboardInterrupt:
        print("End")
