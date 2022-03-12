#!/usr/bin/env python
#-*- coding:utf8 -*-

import socket
host = "10.0.2.15"
port = 21
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)
s.connect((host, port)) # TODO what exception should be foud
print s.recv(4096)
s.send("MESSAGE\n")
