#!/bin/sh

sudo apt-get -y install iperf3
iperf3 -c 127.0.0.1 -i 1 -t 50 -p 5201 -w 300
# Client
# -i 1  # interval of reports
# -t 50 # run for 50 secs
# -w 300  # window?
# Server
# -p 52011


iperf3 -i 1 -s -p 5201  # server
iperf3 -c 127.0.0.1 -i 1 -t 50 -p 5201 -w 300 -b 8M -P 8  # for each client
# I think they can combined in a single command.

