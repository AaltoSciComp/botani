#!/usr/bin/env python3

import sys
import RPi.GPIO as gpio
import iio
import time
import datetime
from influxdb import InfluxDBClient
import json
import logging

MAX_CONNECT_RETRIES = 10

def sample_plants(devs, config):
    gpio.output(config['sensor_power_gpio'], gpio.HIGH)
    time.sleep(1.0)

    for plant in config['plants']:
        dev = devs[plant['sensor']]
        chan = dev.channels[plant['channel']]
        chan.attrs['scale'].value = str(plant['scale'])

    results = {}
    for plant in config['plants']:
        dev = devs[plant['sensor']]
        chan = dev.channels[plant['channel']]
        val = float(chan.attrs['raw'].value)
        results[plant['name']] = val - plant['baseline']

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

    logging.debug(points)
    logging.debug(client.write_points(points))

def main():
    logging.basicConfig(level=logging.INFO)
    config = {}
    for arg in sys.argv[1:]:
        with open(arg) as f:
            config.update(json.loads(f.read()))

    ctx = iio.Context()
    devs = list(filter(lambda dev: dev.name == "ads1015", ctx.devices))
    if (len(devs) == 0):
        logging.error("no iio devices found")

    gpio.setmode(gpio.BOARD)
    gpio.setup(config['sensor_power_gpio'], gpio.OUT)

    while i in range(MAX_CONNECT_RETRIES):
        try:
            client = InfluxDBClient(**config['influxdb'])
            break
        except requests.exceptions.ConnectionError:
            time.sleep((i + 1) * 5)
            continue

    db_name = config['influxdb']['database']
    if {'name': db_name} not in client.get_list_database():
        client.create_database(db_name)
    client.switch_database(db_name)

    try:
        while True:
            moisture_data = sample_plants(devs, config)
            logging.debug(moisture_data)

            db_log(client, moisture_data)
            time.sleep(config['sampling_interval'])
    finally:
        gpio.cleanup()

if __name__ == "__main__":
    main()
