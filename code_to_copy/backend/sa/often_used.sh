echo "XXX" | mail -a "From: XXX@XXX.XXX" -s "XXX" 


# BEGIN 远程挂载
apt-get install sshfs
sshfs root@opvm:/ /mnt/opvm/
umount /mnt/opvm/
# END   远程挂载



