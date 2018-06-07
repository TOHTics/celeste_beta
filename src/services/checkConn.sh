#!/bin/bash
set -e

python /home/pi/Documents/celeste_beta/src/services/wait_network.py > /home/pi/Documents/celeste_beta/src/services/wait_network.log
sleep 60
#sudo ifconfig wwan0 down
#sleep 1
#sudo ifconfig wlan0 down
#sleep 1
#sudo wvdial &
#sleep 13
#sudo route add default dev ppp0 #not use
#sleep 1
#python /home/pi/Documents/celeste_alpha/demos/inversionistas/main.py A001 > /home/pi/Documents/celeste_alpha/demos/inversionistas/out.log
#sleep 20
supervisord #launch the monitoring tool supervisor which run the main measurement power process, check /etc/supervisord.conf

#(
#	while : ; do
#		sudo ifconfig wwan0 down
#		sleep 1
#		sudo wvdial
#		sleep 10
#	done
#) &
#python TaxiClient.py &
