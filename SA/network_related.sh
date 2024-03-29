#!/bin/bash

# =======BEGIN config network  查看网络信息
netstat -nltp
netstat -na # 查看所有链接， 可以加-p看是哪个程序做的连接
# l 表示显示 foreign address 是'0.0.0.0:*' 的连接, a表示显示所有并且会包含l


sudo ethtool  eno1  # 可以查看一些网卡的硬件信息， Link detected: yes能看出网卡有没有插网线
cat /sys/class/net/eno1/carrier  # 同样可以看是否插了网线

# =======END   config network



# =======BEGIN config network
route -n
brctl show

route del/add -net CIDR gw 192.168.1.1
route del/add -host IP gw 192.168.1.1
route del/add default gw 192.168.1.1

# 重启网卡，在ubuntu上会读取 /etc/network/interfaces, 所以修改后用这个命令生效比较好
sudo ifdown eth0 && sudo ifup eth0 # ifup is a script,  include check config and using DHCP
# ifdown和ifup其实是一个脚本, 如果手动配置过需要清除之前的信息， 见 backend/etc/network/interfaces
# - 如果想强行配置可以用 `ifconfig eth0 down` 这种命令处理一下

dhclient eth0 # 如果上面有问题，则用这个获取ip地址

# 给网络起别名
sudo ifconfig eth1:1 192.168.110.123 broadcast 192.168.111.255 netmask 255.255.240.0 up
ip addr add/del <CIDR> [scope link] dev <DEV> # 不加label的话，用 ip addr list 查看


# 设置无线网
# 1) 确认能搜索到网络 && 驱动加载了
iwlist scan


# SELinux
# selinux默认是关闭外部各种端口连接的，需要自己去开
firewall-cmd --permanent --add-port=XXX_PORT/tcp
firewall-cmd --reload
setsebool -P nis_enabled 1

# 如何关闭selinux
vim /etc/selinux/config  # 设置成disable
setenforce 0  # 关闭selinux
sestatus  # 查看状态；   我发现这时还是显示为enabled
# 我看到必须重启之后才能让selinux生效

# =======END   config network



# =======BEGIN 如何关闭防火墙

# CentOS 7.2
systemctl list-unit-files  # 查看所有服务状态
systemctl status firewalld.service  # 检查防火墙状态
systemctl stop firewalld.service   # 关闭防火墙
systemctl disable firewalld.service   # 禁止防火墙
# 其他版本如何关闭防火墙 http://www.jb51.net/article/101576.htm

# =======END   如何关闭防火墙



# =======BEGIN iptables
# 换个端口
# iptables -t nat -A PREROUTING -p tcp --dport FROM_XXX_PORT -j REDIRECT --to-ports TO_XXX_PORT
# 这个成功过， 不需要 设置 route_localnet 也能成功
# iptables -t nat -A PREROUTING -i eth1 -p tcp --dport FROM_XXX_PORT -j DNAT --to-destination XXX_HOST:XXX_PORT
# 这个成功过， 反向代理到localhost需要设置 route_localnet， 但是不确定是否要设置 ip_forward

#
# 可能要做的设置
# # ip_forward : 是否可以forward??? 设置vpn 时需要，反向代理到 localhost时还不确定是否需要
# 看看 cat /proc/sys/net/ipv4/ip_forward
# 确保 /etc/sysctl.conf 中 net.ipv4.ip_forward=1， 然后 sysctl -p
# # route_localnet: 是否可以 route到 localhost
# cat  /proc/sys/net/ipv4/conf/eth_XXX/route_localnet
# /etc/sysctl.conf 中 net.ipv4.conf.eth_XXX.route_localnet=1
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
export no_proxy=localhost,127.0.0.1,127.0.0.0/8,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,.sock
# after you use
unset https_proxy  http_proxy SOCKS_SERVER no_proxy
# BEGIN polipo ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


# ssh 妙用
# 见： http://blog.trackets.com/2014/05/17/ssh-tunnel-local-and-remote-port-forwarding-explained-with-examples.html

# local port forwarding
ssh -L LOCAL_ADDRESS:LOCAL_PORT:REMOTE_ADDRESS:REMOTE_PORT XXX_USER@XXX_HOST
# 将 XXX_HOST *能访问到的* REMOTE_ADDRESS:REMOTE_PORT，变成能直接从 LOCAL_ADDRESS:LOCAL_PORT 访问。
# 记忆时 -L -R 决定了访问的源端口是在远端还是本地。 然后先是源端口， 后是目标端口。
# -D 其实是 local的一种， 指定一个本地的端口， REMOTE_ADDRESS:REMOTE_PORT 能是任何值

# remote port forwarding
# -R 其实相当于反过来， TODO 还需具体实施 

# 跳板机可以用 -w 登录
# https://tufora.com/tutorials/linux/security/ssh-configuration-for-jump-host

# 所以配合polipo也可以在远方开一个http_proxy(本来只有那边本地访问), 然后再ssh -L 转到本地来



# BEGIN nmap VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
nmap -v target.com  # 扫描开了哪些端口 (这个可能只会扫描一下TCP端口或者常用端口)
nmap -sP '10.0.0.*'  # 扫描这个网段的ip
nmap -sT targetHost # 好处是很少有系统会把这种半tcp连接記入日志
nmap -sTU -p PORT HOST  # 扫描指定服务器的的指定端口的TCP和UDP协议
# 详情参见 http://dev.firnow.com/course/6_system/linux/Linuxxl/2007211/14170.html
# BEGIN nmap ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


# config DHCP server
# [DHCP server](http://www.tuicool.com/articles/AzEbii)
sudo apt-get install isc-dhcp-server -y



# BEGIN nc VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
# - sudo apt install netcat

# 看UDP端口的连接性https://serverfault.com/a/733921
# - Server端
nc -ul 4500
# - Client端
nc -u <server> 4500
# - client输入什么回车后， server端输出什么

# END   nc ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


