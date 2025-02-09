import serial
import time
from bitarray import bitarray

# Configure the serial connection
SERIAL_PORT = "/dev/ttyACM0"  # Adjust this if needed
BAUD_RATE = 921600            # Adjust to match your device's settings
TIMEOUT = 1                   # Timeout in seconds

arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT, )
time.sleep(2)

def send_serial(data):
    # Send the data
    arduino.write(data.tobytes())
    print(f"Sent {len(data.tobytes())} bytes to {SERIAL_PORT}")

    # Give some time to process
    time.sleep(0.1)

    # Optional: Wait for a response (if needed)
    # response = arduino.read_until()  # Read up to 64 bytes
    # if response:
    #     print(f"Received: {response.__bytes__()} ({len(response.__bytes__())} bytes)")

if __name__ == "__main__":
    while(True):
        data = bitarray('0' * 64) + bitarray('1' * 64) + bitarray('0' * 256) + bitarray('0' * 64) + bitarray('1' * 64)
        send_serial(data)
        data = bitarray('1' * 64) + bitarray('0' * 64) + bitarray('0' * 256) + bitarray('1' * 64) + bitarray('0' * 64)
        send_serial(data)
        data = bitarray('0' * 64) + bitarray('0' * 64) + bitarray('1' * 256) + bitarray('0' * 64) + bitarray('0' * 64)
        send_serial(data)
        data = bitarray('1' * 64) + bitarray('1' * 64) + bitarray('0' * 256) + bitarray('1' * 64) + bitarray('1' * 64)
        send_serial(data)