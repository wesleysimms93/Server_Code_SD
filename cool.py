import sys
import spidev
import RPi.GPIO as GPIO
import time
import Support

def main():
    if len(sys.argv) < 2:
        print("No action provided")
        return

    action = sys.argv[1]
    if action == 'up':
        print("Moving up")
    elif action == 'down':
        print("Moving down")
    elif action == 'left':
        print("Moving left")
    elif action == 'right':
        print("Moving right")
    elif action == 'home':
        print("Returning to home position")
    elif action == 'emergency_stop':
        print("Emergency stop activated!")
    else:
        print(f"Unknown action: {action}")
    #!/usr/bin/python


    # GPIO setup
    INPUT_PIN = 5  # Replace with your GPIO pin number
    GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbering
    GPIO.setup(INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set as input with pull-down resistor

    OUTPUT_PIN = 6  # Replace with your GPIO pin number
    GPIO.setup(OUTPUT_PIN, GPIO.OUT, initial=GPIO.HIGH)  # Set as input with pull-down resistor

    def send_spi_data_unchecked(data):
        spi = spidev.SpiDev()
        spi.open(0, 1)  # Open SPI bus (bus 0, device 0)
        spi.mode = 0b00
        spi.max_speed_hz = 4800  # Set speed (adjust as necessary)

        spi.writebytes(data)  # Transfer data (list containing one byte)
        w = spi.readbytes(1)

        total_sum = sum(data)
        checksum = total_sum % 256

        print(f"Check Sum is: {checksum}")
        print(f"Returned: {w}")
        if w[0] != checksum:
            print("Failed to send data correctly.")
        spi.close()

    def parse_gcode_command(command, char):
        """Parse a single G-code command into a Support.Point object."""
        return Support.Point.create_from_gcode(command, char)

    try:
        char = 1
        # Prompt the user for G-code commands
        user_input = action

        try:
            print (f"Processing command: {user_input}")
            # Parse the user input into a Support.Point object
            point = parse_gcode_command(user_input, char)
            char += 1
            print(f"Parsed Point: {point}")
            # Wait for GPIO input to go HIGH
            print("Waiting for GPIO input to go HIGH...")
            while GPIO.input(INPUT_PIN) == GPIO.LOW:
                time.sleep(0.01)  # Avoid busy-waiting

            # Send the parsed G-code command
            print("Sending - LOW")
            GPIO.output(OUTPUT_PIN, GPIO.LOW)
            send_spi_data_unchecked(point.point_data_bytes())
            GPIO.output(OUTPUT_PIN, GPIO.HIGH)
            print("Received - HIGH")
            time.sleep(2)

        except Exception as e:
            print(f"Error processing command: {e}")

    finally:
        # Clean up resources
        GPIO.cleanup()

if __name__ == "__main__":
    main()