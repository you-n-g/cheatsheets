
# 测试邮件连通性
echo "XXX" | mail -a "From: XXX@XXX.XXX" -s "XXX" 


# BEGIN 远程挂载
apt-get install sshfs
sshfs root@opvm:/ /mnt/opvm/
umount /mnt/opvm/
# 如果默认指定key挂载(如用root操作)
# Host *
#     IdentityFile /home/young/.ssh/id_rsa


# END   远程挂载



