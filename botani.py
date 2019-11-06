#!/usr/bin/env python3

import RPi.GPIO as gpio
import iio
import time
import datetime
from influxdb import InfluxDBClient
import json

ADS_1115_SCALE = '0.1875'

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

def db_log(client, measurements):
    points = []
    for (plant, moisture) in measurements.items():
        point = {
            'time': str(datetime.datetime.utcnow()),
            'measurement': 'plant-moisture',
            'tags': {
                'plant': plant
            },
            'fields': {
                'value': float(moisture)
            }
        }
        points.append(point)

    print(points)
    print(client.write_points(points))

def main():
    with open('botani.conf') as f:
        config = json.loads(f.read())

    ctx = iio.Context()
    devs = list(filter(lambda dev: dev.name == "ads1015", ctx.devices))
    if (len(devs) == 0):
        print("no iio devices found")

    gpio.setmode(gpio.BOARD)
    gpio.setup(config['sensor_power_gpio'], gpio.OUT)

    client = InfluxDBClient(**config['influxdb'])

    db_name = config['influxdb']['database']
    if {'name': db_name} not in client.get_list_database():
        client.create_database(db_name)
    client.switch_database(db_name)

    try:
        while True:
            moisture_data = sample_plants(devs, config)
            print(moisture_data)

            db_log(client, moisture_data)
            time.sleep(config['sampling_interval'])
    finally:
        gpio.cleanup()

if __name__ == "__main__":
    main()
