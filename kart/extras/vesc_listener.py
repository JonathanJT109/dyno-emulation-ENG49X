import sys
import time

import serial

import pyvesc
from pyvesc import VESC
from tools import choose_port

# float 16: h
# float 32: i
# int: i 1
# char: c 0
# uint: i 1


class GetMCCONF(metaclass=pyvesc.VESCMessage):
    id = 91
    fields = [
        ("l_current_min_scale", "i", 1),
        ("l_current_max_scale", "i", 1),
        ("l_min_erpm", "i", 1),
        ("l_max_erpm", "i", 1),
        ("l_min_duty", "i", 1),
        ("l_max_duty", "i", 1),
        ("l_watt_min", "i", 1),
        ("l_watt_max", "i", 1),
        ("l_in_current_min", "i", 1),
        ("l_in_current_max", "i", 1),
        ("si_motor_poles", "c", 1),
        ("si_gear_ratio", "i", 1),
        ("si_wheel_diameter", "i", 1),
    ]


def main():
    try:
        port = choose_port()

        with VESC(serial_port=port) as ser:
            print(f"Listening on port {port}...")
            msg = GetMCCONF()
            print(msg.id)
            enc = pyvesc.encode_request(msg)
            len = msg._full_msg_size
            print(len)

            while True:
                print("Sending...")
                # Check if there is data waiting to be read
                a = ser.write(enc, 60)
                print(a)

                time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()

