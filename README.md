# Raspberry Pi Water Sensor with Prometheus Metrics

A Python application that reads data from a water sensor connected to a Raspberry Pi and exposes the readings as Prometheus metrics.

## Inspiration

This was inspired by [this newbiely tutorial](https://newbiely.com/tutorials/raspberry-pi/raspberry-pi-rain-sensor). 

## Hardware Requirements

 - Raspberry Pi
 - ["Rain" sensor and ADC](https://www.amazon.com/dp/B0DHGNQZ6X?linkCode=sl1&tag=zlufy-20&linkId=d6c3b90b94272148cb801cf57015b64e&language=en_US&ref_=as_li_ss_tl&th=1)
 - Jumper wires
 - Generic standoffs and baseplates for case

## Pin Configuration

 - POWER_PIN = GPIO 12
 - DO_PIN = GPIO 7

## Installation

```
git clone https://github.com/art12354/raspi_water_sensor_prometheus.git
cd raspi_water_sensor_prometheus
python3 -m venv venv
source venv/bin/activate
pip install RPi.GPIO
pip install prometheus_client
```

Now adjust the water_sensor.service file to match your path to the download location.Then copy the service file to systemd, restart systemd, enable the service to start on boot, and finally start it.

```
sudo cp water_sensor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable water_sensor.service
sudo systemctl start water_sensor.service
```

Sensor data will now be available at http://{raspi_ip_address}:8000/metrics.
