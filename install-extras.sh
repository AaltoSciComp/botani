#!/bin/sh

SYSTEMD_UNIT_DIR=$(pkg-config --variable=systemdsystemunitdir systemd)
install -D botani.service $SYSTEMD_UNIT_DIR
install -D ads1115-i2c.service $SYSTEMD_UNIT_DIR
install -D botani-influxdb.conf /etc/botani/influxdb.conf
install -D botani-plants.conf /etc/botani/plants.conf
