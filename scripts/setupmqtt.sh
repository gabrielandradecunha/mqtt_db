#!/bin/bash

# setup mosquitto and database

function configFiles(){
    cd ../mosquitto/config/
    touch pass
}

function setupMosquittoAndDb(){
    cd ../../../
    sudo docker-compose up -d
}

function createUser(){
    sudo docker exec -it mosquitto mosquitto_passwd -c /mosquitto/config/pass teste
}

configFiles
setupMosquittoAndDb
createUser
