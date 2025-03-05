import RPi.GPIO as GPIO
import time
from prometheus_client import start_http_server, Gauge

# Define GPIO pins
POWER_PIN = 12  # GPIO pin that provides power to the water sensor
DO_PIN = 7     # GPIO pin connected to the DO pin of the water sensor

# Create Prometheus metrics
WATER_DETECTED = Gauge('water_detected', 'Water detection status (1=detected, 0=not detected)')
SENSOR_READ_COUNT = Gauge('water_sensor_read_count', 'Number of times the rain sensor has been read')

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(POWER_PIN, GPIO.OUT)  # configure the power pin as an OUTPUT
    GPIO.setup(DO_PIN, GPIO.IN)

    start_http_server(8000)
    print("Prometheus metrics available at http://localhost:8000/metrics")

def read_sensor():
    GPIO.output(POWER_PIN, GPIO.HIGH)  # turn the water sensor's power ON
    time.sleep(0.01)                   # wait 10 milliseconds

    water_state = GPIO.input(DO_PIN)

    GPIO.output(POWER_PIN, GPIO.LOW)  # turn the water sensor's power OFF

    # Increment the read counter
    SENSOR_READ_COUNT.inc()

    return water_state

def loop():
    water_state = read_sensor()

    if water_state == GPIO.HIGH:
        print("Water is NOT detected")
        WATER_DETECTED.set(0) # Update the Prometheus metric
    else:
        print("Water is detected")
        WATER_DETECTED.set(1) # Update the Prometheus metric

    time.sleep(60)  # pause for 1 minute to avoid reading sensors frequently and prolong the sensor lifetime

def cleanup():
    GPIO.cleanup()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except Exception as e:
        print(f"Error: {e}")
        cleanup()

