#!/bin/bash




# =======BEGIN config network 
route -n
brctl show

route del/add -net CIDR gw 192.168.1.1
route del/add -host IP gw 192.168.1.1
route del/add default gw 192.168.1.1

ifup eth0 # ifup is a script,  include check config and using DHCP 
# =======END   config network 






# =======BEGIN iptables 
# 换个端口
# iptables -t nat -A PREROUTING -p tcp --dport FROM_XXX_PORT -j REDIRECT --to-ports TO_XXX_PORT
# =======END   iptables 






# =======BEGIN HAproxy TCP负载均衡

# this config needs haproxy-1.1.28 or haproxy-1.2.1
global
	log 127.0.0.1	local0
	log 127.0.0.1	local1 notice
	#log loghost	local0 info
	maxconn 4096
	#chroot /usr/share/haproxy
	user haproxy
	group haproxy
	daemon
	#debug
	#quiet

defaults
	log	global
	mode	http
	option	httplog
	option	dontlognull
	retries	3
	option redispatch
	maxconn	2000
	contimeout	5000
	clitimeout	50000
	srvtimeout	50000

listen XXX
        bind 0.0.0.0:90
        mode tcp
        option tcplog
        server s1 127.0.0.1:9090
        server s2 127.0.0.1:9091
        server s2 127.0.0.1:9092
#TODO log
# =======END   HAproxy TCP负载均衡

