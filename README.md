# com.haislund.homeassistant.alsavo

Debian Docker image that publishes states to MQTT and description of how to configure Home Assistant to use the values.

# Docker container
An already build image is available at Docker Hub: peterhaislund/alsavo_status

## Topics
- stat/pool/water_in_temp
- stat/pool/water_out_temp
- stat/pool/ambient_temp
- stat/pool/fan_speed
- stat/pool/heating
- stat/pool/target_temp
- stat/pool/power_mode

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
Serial number for the Alsavo heat pump

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

# Home Assistant Configuration
Manually create sensors for representing each value published through the MQTT Broker.

*To be updated*
