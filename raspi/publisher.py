#!/usr/bin/env python3
import serial
import time
import random

# Import necessary Modules
import os
from google.cloud import pubsub_v1
import time
from random import randrange

#import 3rd api SMHI
from smhi_open_data import SMHIOpenDataClient, Parameter

# Create an object for publishing
publisher = pubsub_v1.PublisherClient()

# Define topic path
topic_path = 'projects/{project_id}/topics/{topic}'.format(
    project_id=os.getenv('PROJECT_ID'), topic=os.getenv('TOPIC_NAME'))

# Initialise temperature and humidity values with 0.0
Outsidetemperature=0.0
Outsidehumidity=0.0
temperature = 0.0
humidity = 0.0

#init smhi client
client = SMHIOpenDataClient()

# # Get closest station
# closest_station = client.get_closest_station(
#     latitude=59.3293,
#     longitude=18.0686)
# print(closest_station)  // get stockholm id=98210

# Set serial to read when arduino signal comes in
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1.0)
time.sleep(3)
ser.reset_input_buffer()
print("Serial OK.")


def getSMHIapi():
    # Get available parameters at station
    parameters_station = client.get_station_parameters(station_id=98210,
                                                       parameter_set=[Parameter.TemperaturePast1h, Parameter.Humidity])

    for each in parameters_station: # type enum
        if each.name=="Humidity": Outsidehumidity=each.value
        else: Outsidetemperature=each.value
    return [Outsidetemperature, Outsidehumidity]


# Execute this loop forever until terminated by the user or
# the raspberry pi fails
while True:
    try:
        time.sleep(0.01)
        if ser.in_waiting > 0:
            msg = ser.readline().decode('utf-8').rstrip()
            msgarr = msg.split("::")
            if len(msgarr)==2 : # has both params from arduino
                [temperature_tmp, humidity_tmp] = msgarr
                temperature = float(temperature_tmp)
                humidity = float(humidity_tmp)
                [Outsidetemperature, Outsidehumidity]=getSMHIapi()
                # Define the structure of payload
                payload ='{{ "data":"PayloadData", "Timestamp":{}, "Temperature":{:3.2f}, "Humidity":{:3.0f}, "Outsidetemperature":{:3.2f}, "Outsidehumidity":{:3.0f} }}'.format(int(time.time()), temperature, humidity, Outsidetemperature, Outsidehumidity)

                # Publish the payload to the cloud
                publisher.publish(topic_path, data=payload.encode('utf-8'))

                print("Publishing the payload : " + payload)

    # In case of keyboard interruption or system crash, raise these exceptions
    except (KeyboardInterrupt, SystemExit):
        print("Close serial communication.")
        ser.close()
        raise
