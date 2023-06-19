#!/usr/bin/env bash                                                                                                         
LOGFILE="/alsavo.log"                                                                                                          
TIMESTAMP=`date "+%Y-%m-%d %H:%M:%S"`                                                                                       
echo "$TIMESTAMP Updating status" >> $LOGFILE                                                                               
/AlsavoCtrl/AlsavoCtrl -s "$alsavo_serial" -l "$alsavo_password" | python3 /mqpublish.py "$mqtt_server" "$mqtt_server_port" "$mqtt_server_user" "$mqtt_server_password"
echo "$TIMESTAMP Update finished" >> $LOGFILE