#!/bin/bash




# =======BEGIN config network 
route -n
brctl show

route del/add -net CIDR gw 192.168.1.1
route del/add -host IP gw 192.168.1.1
route del/add default gw 192.168.1.1

ifup eth0 # ifup is a script,  include check config and using DHCP 
dhclient eth0 # 如果上面有问题，则用这个获取ip地址

# 给网络起别名
sudo ifconfig eth1:1 192.168.110.123 broadcast 192.168.111.255 netmask 255.255.240.0 up
ip addr add/del <CIDR> [scope link] dev <DEV> # 不加label的话，用 ip addr list 查看


# 设置无线网
# 1) 确认能搜索到网络 && 驱动加载了
iwlist scan 

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






# BEGIN polipo VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
sudo apt-get install polipo

# conifg 这里是要将http proxy套在socket proxy上，因为有的应用无法直接使用socket代理
proxyAddress = "127.0.0.1"
proxyPort = 6489
socksParentProxy = "127.0.0.1:8964"
socksProxyType = socks5

# when you want to use
export http_proxy=127.0.0.1:6489  # don't capitalize it !!!!
export https_proxy=127.0.0.1:6489  # don't capitalize it !!!!
export SOCKS_SERVER=127.0.0.1:8964
# after you use
unset https_proxy  http_proxy SOCKS_SERVER
# BEGIN polipo ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


# ssh 妙用
ssh -L LOCAL_ADDRESS:LOCAL_PORT:REMOTE_ADDRESS:REMOTE_PORT XXX_USER@XXX_HOST
# 所以配合polipo也可以在远方开一个http_proxy, 然后再ssh -L 转到本地来

