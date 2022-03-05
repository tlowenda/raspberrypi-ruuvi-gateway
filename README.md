# raspberrypi-ruuvi-gateway
This project uses Raspberry Pi as a gateway to push Ruuvi data to InfluxDB 1.8+ database.

## Prerequisite steps for Raspberry Pi
Setting up the permissions of Bluetooth adapter of Raspberry Pi is as follows
```shell
  sudo apt install bluez bluez-hcidump
  sudo setcap 'cap_net_raw,cap_net_admin+eip' `which hcitool`
  sudo setcap 'cap_net_raw,cap_net_admin+eip' `which hcidump`
```
## Install InfluxDB on Raspberry Pi
```shell
  wget https://dl.influxdata.com/influxdb/releases/influxdb_1.8.10_armhf.deb
  sudo dpkg -i influxdb_1.8.10_armhf.deb
```
Start influx console with influx, and create database for ruuvi measurements with command CREATE DATABASE ruuvi
