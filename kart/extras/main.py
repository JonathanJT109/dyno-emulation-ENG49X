from multiprocessing import Process
from time import sleep

import pandas as pd
from pyvesc import VESC
from pyvesc.VESC.VESC import GetValues

from .pid import PIDController
from .tools import process_data, rpm_to_dist

LAPS = 10
MAX_VOLTAGE = 5.0
MIN_VOLTAGE = 0.0
DIAMETER = 0.254  # TODO: Find diameter
KART_RESPONSE_RATE = 0.001
DYNO_RESPONSE_RATE = 0.001
max_rpm: float = 0  # TODO: How to find max speed?
current_dyno_rpm: float = 0
send_voltage: float = 0
seg_length: float = 0


# Talk to dyno
# WARNING: Is it good way to handle length?
def dyno_info(port: str):
    global current_dyno_rpm
    global seg_length

    with VESC(serial_port=port) as dyno:
        while True:
            measurements = dyno.get_measurements()

            if isinstance(measurements, GetValues):
                current_dyno_rpm = measurements.rpm
                seg_length -= rpm_to_dist(
                    measurements.rpm, DIAMETER, DYNO_RESPONSE_RATE
                )
                sleep(DYNO_RESPONSE_RATE)


# Calculate speed to go in straight lanes before turning
def turn(target_rpm: float, pid: PIDController):
    global send_voltage
    global current_dyno_rpm
    global seg_length

    current_rpm: float = 0.0
    voltage = 0.0

    print("Step\tRPM Setpoint\tCurrent RPM\tVoltage")
    print("-" * 60)

    loop_i = 0
    while seg_length > 0:
        voltage = pid.compute(target_rpm, current_rpm)

        # TODO: Send voltage to controller
        send_voltage = voltage

        current_rpm = current_dyno_rpm

        if loop_i == 0:
            print(f"{loop_i}\t{target_rpm:.1f}\t\t{current_rpm:.1f}\t\t{voltage:.2f}")
        loop_i = (loop_i + 1) % 10
        sleep(KART_RESPONSE_RATE)


def straight():
    global send_voltage
    global seg_length

    while seg_length > 0:
        send_voltage = 5.0
        sleep(KART_RESPONSE_RATE)


# Race
def racing(instructions):
    global seg_length
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

    # Settings processors
    dyno = Process(target=dyno_info)
    dyno.start()

    n_lap = LAPS
    while n_lap > 0:
        print(f"Lap {LAPS - n_lap}")
        for _, length, radius in instructions:
            seg_length = length
            if radius == 0:
                # Full throttle
                # TODO: Calculate brake force to achieve certain speed
                straight()
            else:
                # TODO: Calculate target rpm
                target_rpm = 1500.0
                turn(target_rpm, pid)
        n_lap -= 1

    dyno.join()


if __name__ == "__main__":
    data = process_data("./test.csv")
    racing(data)
