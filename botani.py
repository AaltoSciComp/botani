#!/usr/bin/env python3

import RPi.GPIO as gpio
import iio

def main():
    ctx = iio.Context()
    for dev in ctx.devices:
        print(dev.name)

if __name__ == "__main__":
    main()
