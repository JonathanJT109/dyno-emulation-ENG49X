import pyvesc
import serial
from tools import choose_port
import time

def main():
    try:
        port = choose_port()
        
        with serial.Serial(port=port, baudrate=115200, timeout=0.05) as ser:
            print(f"Listening on port {port}...")
            
            while True:
                # Check if there is data waiting to be read
                if ser.in_waiting:
                    # Read all available bytes
                    buffer = ser.read(ser.in_waiting)
                    
                    # Try to decode the message
                    msg, consumed = pyvesc.decode(buffer)
                    
                    # If we got a valid message, print it
                    if msg:
                        print(f"Received message: {msg.__class__.__name__}")
                        print(msg)
                        # Print all attributes of the message
                        for attr_name in dir(msg):
                            if not attr_name.startswith('_'):  # Skip internal attributes
                                attr_value = getattr(msg, attr_name)
                                if not callable(attr_value):  # Skip methods
                                    print(f"  {attr_name}: {attr_value}")
                
                time.sleep(0.01)
                
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 