#!/bin/bash

pwd
whoami

apt-get update

# "-r" mean restart
if [ "$1" != "-r" ]; then

  # Docker-compose install and run

  apt -y install docker.io docker-compose
  systemctl start docker
  systemctl enable docker

  apt-get install jq
  
  # config.json generation

  cp app/config_example.json app/config.json

  read -p 'token for the telegram bot: ' token
  jq -c --arg a "$token" '.token = $a' app/config.json > tmp.$$.json && mv tmp.$$.json app/config.json

  read -p 'db_client_id for the application: ' db_client_id
  jq -c --arg a "$db_client_id" '.db_client_id = $a' app/config.json > tmp.$$.json && mv tmp.$$.json app/config.json

  read -p 'db_client_secret for the application: ' db_client_secret
  jq -c --arg a "$db_client_secret" '.db_client_secret = $a' app/config.json > tmp.$$.json && mv tmp.$$.json app/config.json

  read -p 'db_address - database api address: ' db_address
  jq -c --arg a "$db_address" '.db_address = $a' app/config.json > tmp.$$.json && mv tmp.$$.json app/config.json

  read -p 'db_username - Username in ozma: ' db_username
  jq -c --arg a "$db_username" '.db_username = $a' app/config.json > tmp.$$.json && mv tmp.$$.json app/config.json

  read -p 'db_password - Password in ozma: ' db_password
  jq -c --arg a "$db_password" '.db_password = $a' app/config.json > tmp.$$.json && mv tmp.$$.json app/config.json

  read -p 'db_schema_name - Schema in ozma: ' db_schema_name
  jq -c --arg a "$db_schema_name" '.db_schema_name = $a' app/config.json > tmp.$$.json && mv tmp.$$.json app/config.json

  read -p 'db_view_name - View in ozma: ' db_view_name
  jq -c --arg a "$db_view_name" '.db_view_name = $a' app/config.json > tmp.$$.json && mv tmp.$$.json app/config.json
  
  # list.json generation
  
  cp app/list_example.json app/list.json
  
  read -p 'tg_id for user with access: ' tg_id
  jq -c --arg a "$tg_id" '.list[0].tg_id = $a' app/list.json > tmp.$$.json && mv tmp.$$.json app/list.json

fi

sudo docker-compose up --build
