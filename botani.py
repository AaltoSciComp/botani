#!/usr/bin/env python3

import RPi.GPIO as gpio
import iio
import time

ADS_1115_SCALE = '0.1875'

def sample_plants(devs, config):
    gpio.output(config['sensor_power_gpio'], gpio.HIGH)
    time.sleep(1.0)

    results = {}
    for plant in config['plants']:
        chan = devs[plant['sensor']].channels[plant['channel']]
        chan.attrs['scale'].value = ADS_1115_SCALE
        results[plant['name']] = chan.attrs['raw'].value

    gpio.output(config['sensor_power_gpio'], gpio.LOW)

    return results

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

    print(sample_plants(devs, config))

    gpio.cleanup()

if __name__ == "__main__":
    main()
