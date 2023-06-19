import time                                                                                                                 
import sys                                                                                                                  
import re                                                                                                                   
import os   
import json                                                                                                                
import paho.mqtt.client as mqtt                                                                                             
#import paho.mqtt.publish as publish
from datetime import datetime
import traceback

class mqtt_stub:
  def __init__(self):
    print("No mqtt broker configured - using test stub")
    
  def username_pw_set(self, username, password):
    print("Setting user/pass: " + username + " | " + password)

  def connect(self, broker_server, broker_server_port , timeout):
    print("Connecting to test stub " + broker_server + ":" + str(broker_server_port) + " | " + str(timeout))
    
  def loop_start(self) :
    print("loop_start")
    
  def publish(self, topic, value):
    print("publishing " + topic + " | " + str(value))
    
  def loop_stop(self):
    print("loop_stop")    
    
def main():                                                                                                                 
  with open('/app/mqpublish.log', 'a') as sys.stdout:
    print(datetime.now().strftime("%Y-%m-%d, %H:%M:%S") + " Publishing status")
  
    try: 
      # Status codes
      WATER_IN_TEMP = 16
      WATER_OUT_TEMP = 17
      AMBIENT_TEMP = 18
      FAN_SPEED = 22
      
      #Config codes
      TARGET_TEMP = 1
      POWER_MODE = 16    
      
      # HA topics
      TOPIC_BASE = "stat/pool/"
      
      if not (os.getenv("mqtt_server") == "None"):
        client = mqtt.Client()    
      else:
        client = mqtt_stub()    

      broker_server = os.getenv("mqtt_server")
      broker_server_port = os.getenv("mqtt_server_port")
      broker_user = os.getenv("mqtt_server_user")
      broker_password = os.getenv("mqtt_server_password")
      
      if not (broker_user == "None"):
        client.username_pw_set(broker_user, password=broker_password)
       
      client.connect(broker_server, int(broker_server_port) , 60) 
      client.loop_start()                                                                                                     
      
      inputMissing = True                                                                                                    
      
      for line in sys.stdin:                                                                                                  
        m = re.match('(.*)=(.*)', line)                                                                                       
        if m:                                                                                                                 
          inputMissing = False 
     
          inputObject = json.loads(m.group(2))
          inputType = inputObject["type"]
          inputIndex = inputObject["index"]
          inputValue = inputObject["value"]
          
          if inputType == "status":
            if inputIndex == WATER_IN_TEMP:
              print(datetime.now().strftime("%Y-%m-%d, %H:%M:%S") + " Publishing: WATER_IN_TEMP : " + str(inputValue))
              client.publish(TOPIC_BASE + "water_in_temp", str(inputValue))  
            if inputIndex == WATER_OUT_TEMP:
              print(datetime.now().strftime("%Y-%m-%d, %H:%M:%S") + " Publishing: WATER_OUT_TEMP : " + str(inputValue))
              client.publish(TOPIC_BASE + "water_out_temp", str(inputValue))  
            if inputIndex == AMBIENT_TEMP:
              print(datetime.now().strftime("%Y-%m-%d, %H:%M:%S") + " Publishing: AMBIENT_TEMP : " + str(inputValue))
              client.publish(TOPIC_BASE + "ambient_temp", str(inputValue))  
            if inputIndex == FAN_SPEED:
              print(datetime.now().strftime("%Y-%m-%d, %H:%M:%S") + " Publishing: FAN_SPEED : " + str(inputValue))
              client.publish(TOPIC_BASE + "fan_speed", str(inputValue))  
              
              heating_value = "off"
              
              if inputValue > 0:
                heating_value = "on"
                
              print(datetime.now().strftime("%Y-%m-%d, %H:%M:%S") + " Publishing: HEATING : " + heating_value)
              client.publish(TOPIC_BASE + "heating", heating_value) 
              
          if inputType == "config":
            if inputIndex == TARGET_TEMP:
              print(datetime.now().strftime("%Y-%m-%d, %H:%M:%S") + " Publishing: TARGET_TEMP : " + str(inputValue/10))
              client.publish(TOPIC_BASE + "target_temp", str(inputValue/10))  
            if inputIndex == POWER_MODE:
              print(datetime.now().strftime("%Y-%m-%d, %H:%M:%S") + " Publishing: POWER_MODE : " + str(inputValue))
              client.publish(TOPIC_BASE + "power_mode", str(inputValue))  
     
      if bool(inputMissing):                                                                                                        
        print(datetime.now().strftime("%Y-%m-%d, %H:%M:%S") + " No input received to publish")                                                                      
  
      #  time.sleep(2)                                                                                                        
      client.loop_stop()                                                                                                    
  
    except Exception as inst:
      print(datetime.now().strftime("%Y-%m-%d, %H:%M:%S").join(traceback.TracebackException.from_exception(inst).format()))      

if __name__ == "__main__":                                                                                                  
  main()