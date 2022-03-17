#!/bin/sh

#/usr/bin/spawn-fcgi -a 127.0.0.1 -p 9000 -C 5 -u www-data -g www-data -f /usr/bin/php5-cgi -P /var/run/fastcgi-php.pid
/usr/bin/spawn-fcgi -a 127.0.0.1 -p 9000 -C 5 -u deploy -g deploy -f /usr/bin/php5-cgi -P /var/run/fastcgi-php.pid

su -c"XXX" XXX

/usr/bin/memcached -m XXX -p XXXX -u nobody -l 127.0.0.1 -d


# iptables
iptables -A INPUT -i eth1 -p tcp -s 60.195.252.106 --dport 3306 -j ACCEPT
iptables -A INPUT -i eth1 -p tcp -s 127.0.0.1 --dport 3306 -j ACCEPT
iptables -A INPUT -p tcp -m tcp --dport 3306 -j REJECT

iptables -A INPUT -p tcp -m tcp --dports 27017,28017 -s 121.194.75.128/25 -j ACCEPT
iptables -A INPUT -p tcp -m tcp --dports 27017,28017 -j REJECT
# iptables
