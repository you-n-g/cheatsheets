#!/bin/sh

/usr/bin/spawn-fcgi -a 127.0.0.1 -p 9000 -C 5 -u www-data -g www-data -f /usr/bin/php5-cgi -P /var/run/fastcgi-php.pid

su -c"XXX" XXX

/usr/bin/memcached -m XXX -p XXXX -u nobody -l 127.0.0.1 -d
