#!/bin/sh
modprobe ti-ads1015
echo "ads1115 0x48" > /sys/class/i2c-adapter/i2c-1/new_device
