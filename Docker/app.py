import os.path
import os          
import subprocess 
import sys                                                                                                      
import re  
import time  
from datetime import datetime
import json   
import paho.mqtt.client as mqtt      
import traceback
from logger import logger
from config import Config
  
##########################
### TEST STUB FOR MQTT
##########################
class mqtt_stub:
  def __init__(self):
    logger.log("No mqtt broker configured - using test stub")
    
  def username_pw_set(self, username, password):
    logger.log("Setting user/pass: " + username + " | " + password)

  def connect(self, broker_server, broker_server_port , timeout):
    logger.log("Connecting to test stub " + broker_server + ":" + str(broker_server_port) + " | " + str(timeout))
    
  def loop_start(self) :
    logger.log("loop_start")
    
  def publish(self, topic, value):
    logger.log("publishing " + topic + " | " + str(value))
    
  def loop_stop(self):
    logger.log("loop_stop")    

##########################
### APP FUNCTIONS
##########################
def query_heatpump(heatpump):
    #cmd = "/app/AlsavoCtrl -s "+ heatpump["serial"] + " -l " + heatpump["password"]
    #response = os.popen(cmd).read()
    
    #with open("C:/temp/alsavo.txt") as f:
    #    response = f.readlines()
 
    response = subprocess.check_output(["/app/AlsavoCtrl", "-s", heatpump["serial"], "-l", heatpump["password"]], text=True, universal_newlines=True)
 
    return response

##########################
### APP CODE
##########################
try:
    config_loader = Config()
    config = config_loader.load_config()

    mqtt_config = config["mqtt"]
    
    broker_server = mqtt_config["server"]
    broker_server_port = mqtt_config["server_port"]
    broker_user = mqtt_config["server_user"]
    broker_password = mqtt_config["server_password"]
    
    if not (broker_server == "None") and not (broker_server is None):
        client = mqtt.Client()    
    else:
        client = mqtt_stub()    
    
    if not (broker_user == "None") and not (broker_user is None):
      client.username_pw_set(broker_user, password=broker_password)
      
    client.connect(broker_server, int(broker_server_port) , 60) 
    client.loop_start()  

    while True:
        try: 
            logger.log(datetime.now().strftime("%Y-%m-%d, %H:%M:%S") + " Publishing status")
  
            for heatpump in config["heatpumps"]: 
                response = query_heatpump(heatpump)
                                
                for line in response.split('\n'):
                    m = re.match('(.*)=(.*)', line)     
                    if m:                
                        inputObject = json.loads(m.group(2))
                        inputType = inputObject["type"]
                        inputIndex = inputObject["index"]
                        inputValue = inputObject["value"]
                                        
                        config_topics = config_loader.find_topics(heatpump["topics"], inputType, inputIndex)
                        
                        for config_topic in config_topics:
                            for mapping in config_topic["mappings"]:
                                if not mapping is None:                        
                                    if mapping["type"] == "replace":
                                        for mappingValue in mapping["replacements"]:
                                            if str(inputValue) == (mappingValue["from"]):
                                                inputValue = mappingValue["to"]
                                    if mapping["type"] == "eval":
                                        value = inputValue;
                                        inputValue = eval(mapping["formula"])
                                    
                            logger.log(datetime.now().strftime("%Y-%m-%d, %H:%M:%S") + " Publishing: " + config_topic["topic"] + " : " + str(inputValue))
                            client.publish(config_topic["topic"], str(inputValue)) 
            
        except Exception as inst:
            logger.log(datetime.now().strftime("%Y-%m-%d, %H:%M:%S").join(traceback.TracebackException.from_exception(inst).format()))      

        #Flush log file
        sys.stdout.flush()
                
        time.sleep(int(config["publish_interval"]))

    client.loop_stop()  
  
except Exception as inst:
    logger.log(datetime.now().strftime("%Y-%m-%d, %H:%M:%S").join(traceback.TracebackException.from_exception(inst).format()))   