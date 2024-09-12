# -*- coding: utf-8 -*-
#
# Copyright 2024 Kevin Lindemark
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

"""
links and resources used:
https://thingsboard.io/docs/user-guide/rpc/
https://github.com/manuargue/thingsboard-micropython
https://www.youtube.com/watch?v=EWJAZA_44ro

"""
from uthingsboard.client import TBDeviceMqttClient
from time import sleep
from random import randint, uniform
from machine import reset
import gc
import secrets
from machine import UART
from gps_bare_minimum import GPS_SIMPLE
#########################################################################
# CONFIGURATION
gps_port = 2                               # ESP32 UART port, Educaboard ESP32 default UART port
gps_speed = 9600                           # UART speed, defauls u-blox speed
#########################################################################
# OBJECTS
uart = UART(gps_port, gps_speed)           # UART object creation
gps = GPS_SIMPLE(uart)                    # GPS object creation
#########################################################################     

        
def get_lat_lon():
    lat = lon = None # Opretter variabler med None som værdi
    if gps.receive_nmea_data():
    # hvis der er kommet end bruggbar værdi på alle der skal anvendes
        if gps.get_latitude() != -999.0 and gps.get_longitude() != -999.0 and gps.get_validity() == "A":
            # gemmer returværdier fra metodekald i variabler
            lat = str(gps.get_latitude())
            lon = str(gps.get_longitude())
            # returnerer data med adafruit gps format
            return lat, lon
        else: # hvis ikke både hastighed, latitude og longtitude er korrekte 
            print(f"GPS data to server not valid:\nlatitude: {lat}\nlongtitude: {lon}")
            return False
    else:
        return False
# See examples for more authentication options
client = TBDeviceMqttClient(secrets.SERVER_IP_ADDRESS, access_token = secrets.ACCESS_TOKEN)

# Connecting to ThingsBoard
client.connect()
print("connected to thingsboard, starting to send and receive data")
while True:
    try:
        print(f"free memory: {gc.mem_free()}")
        # monitor and free memory
        if gc.mem_free() < 2000:
            print("Garbage collected!")
            gc.collect()
        
        lat_lon = get_lat_lon()
        print(lat_lon)
        if lat_lon:
            # Sending telemetry        
            telemetry = {'latitude': lat_lon[0], 'longitude': lat_lon[1]}
            client.send_telemetry(telemetry)
        
        # Checking for incoming subscriptions or RPC call requests (non-blocking)
        client.check_msg()
        print(".",end="")
        sleep(1)
    except KeyboardInterrupt:
        print("Disconnected!")
        # Disconnecting from ThingsBoard
        client.disconnect()
        reset()
