import pyvesc
from tools import choose_port
import serial
import time

def main():
    try:
        port = choose_port()
        
        with serial.Serial(port=port, baudrate=115200, timeout=0.05) as ser:
            print(f"Listening on port {port}...")

            message = "Hello"
            encoded = pyvesc.encode(message)
            
            while True:
                ser.write(encoded)
                time.sleep(1)
                
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 
