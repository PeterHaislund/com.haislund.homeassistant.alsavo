#!/usr/bin/env bash 
while [ true ]
do
  /app/AlsavoCtrl -s "$alsavo_serial" -l "$alsavo_password" | python3 /app/mqpublish.py
 
  #truncate log
  echo "$(tail -$log_size /app/mqpublish.log)" > /app/mqpublish.log
  
  sleep $publish_interval
done