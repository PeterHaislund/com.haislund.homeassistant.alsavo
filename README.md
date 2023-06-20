# com.haislund.homeassistant.alsavo

Debian Docker image that publishes states from an Alsavo Heat Pump (taken from the Alsavo Pro Cloud Server) to MQTT and description of how to configure Home Assistant to use the values.

The Docker image uses a compiled version of AlsavoCtrl developed by Mike Strandborg - [GitHub link](https://github.com/strandborg/AlsavoCtrl).

# Docker container
An already build image is available at Docker Hub: peterhaislund/alsavo_status

## Environmental variables
Must be set while creating the docker container through -e variables.

### mqtt_server
Server/IP adress of MQTT Broker to publish to

### mqtt_server_port
*[optional, default 1883]* Port number for MQTT Broker

### mqtt_server_user
*[optional]* User for MQTT Broker

### mqtt_server_password
*[optional]* Password for MQTT Broker

### alsavo_serial
Serial number for the Alsavo heat pump (find it by clicking on the top-right logo in the Alsavo Pro app)

### alsavo_password
Password for the Alsavo heat pump

### publish_interval
*[optional, default 300]* Number of seconds between each status publish

### log_size
*[optional, default 1000]* Number of log lines to retain in app/mqpublish.log

## Running container
Example of creating/running the container:

```
docker image pull peterhaislund/alsavo_status
docker create -e alsavo_serial=XXXXXXXXX -e alsavo_password=XXXXXX -e mqtt_server=192.168.1.128 -e TZ=Europe/Copenhagen --name alsavo_status peterhaislund/alsavo_status
```
# MQTT

## Topics
- stat/pool/water_in_temp
- stat/pool/water_out_temp
- stat/pool/ambient_temp
- stat/pool/fan_speed
- stat/pool/heating
- stat/pool/target_temp
- stat/pool/power_mode

# Home Assistant Configuration
Make sure you have installed [MQTT](https://www.home-assistant.io/integrations/mqtt/) in Home Assistant and it is connected to the MQTT Broker.

Manually create sensors for representing each value published through the MQTT Broker.

As an example: In configuration.yaml add the following (remember to restart afterwards):

```
mqtt:
  sensor:
    - name: "Pool Heater - Water In Temperature"
      unique_id: 347a8fbe-c63c-4360-bffb-855bdae841cb
      state_topic: "stat/pool/water_in_temp"
      state_class: "measurement"
      unit_of_measurement: "°C"
    - name: "Pool Heater - Water Out Temperature"
      unique_id: 01ac6276-4d9e-4940-a63c-d16f8154b249
      state_topic: "stat/pool/water_out_temp"
      state_class: "measurement"
      unit_of_measurement: "°C"
```
