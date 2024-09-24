# GPS program
from machine import UART
from gps_simple import GPS_SIMPLE
import _thread
import time

#########################################################################
# CONFIGURATION
gps_port = 2                               # ESP32 UART port, Educaboard ESP32 default UART port
gps_speed = 9600                           # UART speed, defauls u-blox speed
#########################################################################
# OBJECTS
uart = UART(gps_port, gps_speed)           # UART object creation
gps = GPS_SIMPLE(uart)                    # GPS object creation
#########################################################################    
# PROGRAM

# Dictionary til at opbevare GPS data så det nemt kan tilgås
# Ved at anvende denne undgår man et delay i programmet
# når der ventes på at GPS data kommer over UART
gps_data = {
    "UTC YYYY-MM-DD": 0,
    "UTC HH:MM:SS": 0,
    "longitude" : -999,
    "latitude": -999,
    "validity": "V",
    "speed": 0,
    "course:": 0.0
    }

def gps_tread():
    while True:
        if gps.receive_nmea_data():
            gps_data["UTC YYYY-MM-DD"] = "%04d-%02d-%02d" % (gps.get_utc_year(), gps.get_utc_month(), gps.get_utc_day())
            gps_data["UTC HH:MM:SS"] = "%02d-%02d-%02d" % (gps.get_utc_hours(), gps.get_utc_minutes(), gps.get_utc_seconds())
            gps_data["latitude"] = "%.8f" % gps.get_latitude()
            gps_data["longitude"] = "%.8f" % gps.get_longitude()
            gps_data["validity"] = "%s" % gps.get_validity()
            gps_data["speed"] = "%.1f" % gps.get_speed()
            gps_data["course"] = "%.1f" % gps.get_course()
            print(gps_data,"\n")
    
        time.sleep(1)
 
_thread.start_new_thread(gps_tread, ()) # starter funktionen som en thread

