#!/usr/bin/env python3

import RPi.GPIO as gpio
import iio
import time
from influxdb import InfluxDBClient

ADS_1115_SCALE = '0.1875'
DB_NAME = 'plantdb-test'

def sample_plants(devs, config):
    gpio.output(config['sensor_power_gpio'], gpio.HIGH)
    time.sleep(1.0)

    results = {}
    for plant in config['plants']:
        chan = devs[plant['sensor']].channels[plant['channel']]
        chan.attrs['scale'].value = ADS_1115_SCALE
        results[plant['name']] = float(chan.attrs['raw'].value)

    gpio.output(config['sensor_power_gpio'], gpio.LOW)

    return results

def db_log(client, moisture):
    entry = []
    for (plant, value) in moisture.items():
        print(plant, value)

def db_create(client):
    client.create_database(DB_NAME)

def main():
    config = {
        'sensor_power_gpio': 11,
        'plants': [
            {
                'sensor': 0,
                'channel': 1,
                'scale': 0.1875,
                'name': 'parsa',
            }
        ]
    }

    ctx = iio.Context()
    devs = list(filter(lambda dev: dev.name == "ads1015", ctx.devices))
    if (len(devs) == 0):
        print("no iio devices found")

    gpio.setmode(gpio.BOARD)
    gpio.setup(config['sensor_power_gpio'], gpio.OUT)

    client = InfluxDBClient('localhost', 80)

    if {'name': DB_NAME} not in client.get_list_database():
        db_create(client)

    moisture_data = sample_plants(devs, config)
    print(moisture_data)

    db_log(client, moisture_data)

    gpio.cleanup()

if __name__ == "__main__":
    main()
