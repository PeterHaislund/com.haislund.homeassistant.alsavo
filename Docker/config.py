import json
import os.path
import os  

class Config:
    config_file = "/data/config.json"
    #config_file = "c:/temp/config.json"
    
    def load_config(self):
        self.validate_config()
        
        with open(self.config_file, 'r') as openfile:
            config = json.load(openfile)
    
        return config
    
    def find_topics(self, topic_list, entry_type, index):
        topics = []
        
        for topic in topic_list:
            inputType = topic["type"]
            inputIndex = topic["index"]
          
            if inputType == entry_type and inputIndex == index:
                topics.append(topic)
    
        return topics
        
    def validate_config(self):
        if not os.path.isfile(self.config_file):
            # Generate default config based on ENV variables if config file doesn't exist
            config = {
                "publish_interval": os.getenv("publish_interval"),
                "log_size": os.getenv("log_size"),
                "mqtt": {
                    "server": os.getenv("mqtt_server"),
                    "server_port": os.getenv("mqtt_server_port"),
                    "server_user": os.getenv("mqtt_server_user"),
                    "server_password": os.getenv("mqtt_server_password")
                },
                "heatpumps": [
                    {
                        "serial": os.getenv("alsavo_serial"),
                        "password": os.getenv("alsavo_password"),
                        "topics": [                            
                            {
                                "type": "status",
                                "index": 16,
                                "topic": "stat/pool/water_in_temp",
                                "mappings": []
                            },
                            {
                                "type": "status",
                                "index": 17,
                                "topic": "stat/pool/water_out_temp",
                                "mappings": []
                            },
                            {
                                "type": "status",
                                "index": 18,
                                "topic": "stat/pool/ambient_temp",
                                "mappings": []
                            },
                            {
                                "type": "status",
                                "index": 22,
                                "topic": "stat/pool/fan_speed",
                                "mappings": []
                            },
                            {
                                "type": "status",
                                "index": 22,
                                "topic": "stat/pool/heating",
                                "mappings": [
                                    {
                                        "type": "eval",
                                        "formula": "value>0"
                                    },
                                    {
                                        "type": "replace",
                                        "replacements": [
                                            {
                                                "from": "True",
                                                "to": "on"
                                            },
                                            {
                                                "from": "False",
                                                "to": "off"
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "type": "config",
                                "index": 16,
                                "topic": "stat/pool/power_mode",
                                "mappings": [
                                    {
                                        "type": "replace",
                                        "replacements": [
                                            {
                                                "from": "0",
                                                "to": "Silent"
                                            },
                                            {
                                                "from": "1",
                                                "to": "Smart"
                                            },
                                            {
                                                "from": "2",
                                                "to": "Powerful"
                                            }
                                        ]
                                    }
                                ]
                            },
                            {
                                "type": "config",
                                "index": 1,
                                "topic": "stat/pool/target_temp",
                                "mappings": [
                                    {
                                        "type": "eval",
                                        "formula": "value/10"
                                    }
                                ]
                            },
                        ]
                    }
                ]			
              }
              
            with open(self.config_file, 'a') as outfile:
              json.dump(config, outfile, indent=4)
