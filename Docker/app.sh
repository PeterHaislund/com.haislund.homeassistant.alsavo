#!/usr/bin/env bash 
#LOGFILE="/app/alsavo.log" 
while [ true ]
do
  #TIMESTAMP=`date "+%Y-%m-%d %H:%M:%S"`                                                                                       
  #echo "$TIMESTAMP Updating status" >> $LOGFILE 
  /app/AlsavoCtrl -s "$alsavo_serial" -l "$alsavo_password" | python3 /app/mqpublish.py
  #echo "$TIMESTAMP Update finished" >> $LOGFILE
   
  #truncate log
  echo "$(tail -$log_size /app/mqpublish.log)" > /app/mqpublish.log
  
  sleep $publish_interval
done