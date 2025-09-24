#/bin/bash

# example of topic publish

sudo docker exec -it mosquitto mosquitto_pub -h 127.0.0.1 -p 1883 -t "gps/vivo/cuiaba" -m '{"latitude":"55.75404501486462","longitude":"37.62078427116427","Nivel_agua":"5000","MACAddress":"88:13:BF:68:9F:68","Data":"2025/02/06","hora_cuiaba":"16:40:16"}' -u "teste" -P "teste"
