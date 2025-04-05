import time

import serial

import pyvesc
from tools import choose_port


def main():
    try:
        port = choose_port()

        with serial.Serial(port=port, baudrate=115200, timeout=0.05) as ser:
            print(f"Listening on port {port}...")

            while True:
                if ser.in_waiting:
                    buffer = ser.read(ser.in_waiting)

                    if buffer:
                        print(buffer)

                time.sleep(0.001)

    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
