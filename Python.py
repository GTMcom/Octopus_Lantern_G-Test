import time
import random
from random import randint
from random import seed
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from ina219 import INA219
from ina219 import DeviceRangeError

# You can generate a Token from the "Tokens Tab" in the UI
token = "uTpR5Za6bHzft8zy7tdjODMUbEWNsxijOowQwY16EOag7wBpINrx_88Atimxmx7KOg1v70np0Hx0wJySGn7jow=="
org = "gatemarine"
bucket = "octopusgüçtestbucket"


client = InfluxDBClient(url="http://65.21.107.165:8086", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)

DEBUG = 1
ON = 1
OFF = 0
# Sensor initializations
# adresler octopus adreslerine göre verilecek
# GSMli
ina1 = INA219(0.1, 0.5, address=0x45, busnum=0)
ina1.configure(ina1.RANGE_16V, ina1.GAIN_AUTO)
# GPSliGSMsiz
ina2 = INA219(0.1, 0.5, address=0x45, busnum=0)
ina2.configure(ina2.RANGE_16V, ina2.GAIN_AUTO)
# GPSsiz
ina3 = INA219(0.1, 0.5, address=0x45, busnum=0)
ina3.configure(ina3.RANGE_16V, ina3.GAIN_AUTO)
# SEALITE
ina4 = INA219(0.1, 0.5, address=0x45, busnum=0)
ina4.configure(ina4.RANGE_16V, ina4.GAIN_AUTO)


def get_randomvoltage():
    return randint(0, 10)*0.1 + 12


def get_randomcurrent_on():
    return randint(0, 5)*0.01 + 0.15


def get_randomcurrent_off():
    return randint(0, 5)*0.01+0.03


if(DEBUG == 1):
    def returnlanternpowerdata(ina219_id, measurement_name, device_name, sel):
        if(sel == 1):
            random_voltage = get_randomvoltage()
            random_current = get_randomcurrent_on()
            random_power = random_voltage*random_current
            power_data = {
                "measurement": measurement_name,
                "tags": {
                    "Device": device_name,
                },
                "fields": {
                    "bus_voltage": random_voltage,
                    "current":  random_current,
                    "power": random_power
                }
            }
        else:
            random_voltage = get_randomvoltage()
            random_current = get_randomcurrent_off()
            random_power = random_voltage*random_current
            power_data = {
                "measurement": measurement_name,
                "tags": {
                    "Device": device_name,
                },
                "fields": {
                    "bus_voltage": random_voltage,
                    "current":  random_current,
                    "power": random_power
                }
            }

        return power_data
else:
    def returnlanternpowerdata(ina219_id, measurement_name, device_name):

        power_data = {
            "measurement": measurement_name,
            "tags": {
                "Device": device_name,
            },
            "fields": {
                "bus_voltage": ina219_id.voltage(),
                "current":  ina219_id.current(),
                "power": ina219_id.power()
            }
        }
        return power_data


def application_start_powertest():
    measurement_period = 0.1
    if(DEBUG == 1):
        for _ in range(20):
            data1 = returnlanternpowerdata(ina1, "power_data", "GSMLANTERN", ON)
            data2 = returnlanternpowerdata(ina2, "power_data", "GPSLANTERN", ON)
            data3 = returnlanternpowerdata(ina3, "power_data", "GPSSİZLANTERN", ON)
            data4 = returnlanternpowerdata(ina4, "power_data", "SEALİTELANTERN", ON)
            time.sleep(measurement_period)
            write_api.write(bucket, org, data1)
            time.sleep(0.001)
            write_api.write(bucket, org, data2)
            time.sleep(0.001)
            write_api.write(bucket, org, data3)
            time.sleep(0.001)
            write_api.write(bucket, org, data4)

        for _ in range(60):

            data1 = returnlanternpowerdata(ina1, "power_data", "GSMLANTERN", ON)
            data2 = returnlanternpowerdata(ina2, "power_data", "GPSLANTERN", ON)
            data3 = returnlanternpowerdata(ina3, "power_data", "GPSSİZLANTERN", ON)
            data4 = returnlanternpowerdata(ina4, "power_data", "SEALİTELANTERN", ON)
            time.sleep(measurement_period)
            write_api.write(bucket, org, data1)
            time.sleep(0.001)
            write_api.write(bucket, org, data2)
            time.sleep(0.001)
            write_api.write(bucket, org, data3)
            time.sleep(0.001)
            write_api.write(bucket, org, data4)

    else:
        data1 = returnlanternpowerdata(ina1, "power_data", "GSMLANTERN", ON)
        data2 = returnlanternpowerdata(ina2, "power_data", "GPSLANTERN", ON)
        data3 = returnlanternpowerdata(ina3, "power_data", "GPSSİZLANTERN", ON)
        data4 = returnlanternpowerdata(ina4, "power_data", "SEALİTELANTERN", ON)
        time.sleep(measurement_period)
        write_api.write(bucket, org, data1)
        time.sleep(0.001)
        write_api.write(bucket, org, data2)
        time.sleep(0.001)
        write_api.write(bucket, org, data3)
        time.sleep(0.001)
        write_api.write(bucket, org, data4)


while(1):
    application_start_powertest()

