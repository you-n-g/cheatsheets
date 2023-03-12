#!/usr/bin/env bash

# 目录
# - 分区管理
# - 查看信息
# - 清理垃圾文件
# - 其他


# BEGIN 分区管理 ==================================

# 0) 查看硬盘
fdisk -l

# 1) 先分区
fdisk  /dev/sda #注意是对整个disk而不是分区
# 常用命令
p # 打印分区表
n # 新建分区表
w # 写入分区表
t # 创建swap分区时需要指定 system id??
# fdisk不能创建2TB以上的分区

# 2) 创建文件系统
mkfs.ext4 /dev/xvdb1 # 注意是分区,   这个我后来试过其实不需要是分区也可以有用
mkswap /dev/xvdb1 # swapon /dev/xvdb1 来挂载分区


# 3) /etc/fstab
# man fstab 中有详细的说明
# 分区 路径 文件系统 挂载参数(普通的都用defaults) 是否需要备份(一般是不需要,用0)  自检顺序(0不需自检，/应该为1，其他分区为2)
/dev/xvdb1 /data/                   ext4    defaults        0 2
/dev/xvdb2 none            swap    sw              0       0
# mount -a 会自动挂载fstab中的东西，  可以以此检测:  可以不重启也启动
# https://serverfault.com/a/174182


# 分区扩展 
# 删除该分区, 然后再创建同一起始扇区， 任意结束扇区的分区， 数据会被保留
# 感觉很危险， 不知道可不可信 http://litwol.com/content/fdisk-resizegrow-physical-partition-without-losing-data-linodecom

# END   分区管理 ==================================




# BEGIN 查看信息

# get block size
blockdev --getbsz /dev/sda1 

# get all info
tunefs -l /dev/sda1 # 只针对ext2/3/4

# 解读fdisk -l
blocks 按 1024 byte 计算 ？？？？ why!!! 这不跟 blockdev 冲突了么？？
begin end 按 unit 计算 ????



# 查看磁盘类型： ssd or HDD
# https://unix.stackexchange.com/a/65602
lsblk -d -o name,rota   # 列出所有disk的 name和rota属性
cat /sys/block/sda/queue/rotational   # 列出 sda 的rotational属性

# END 查看信息





# BEGIN 清理垃圾文件  -----------------------

ncdu
# -x :  不跨越文件系统的边界
# https://www.ostechnix.com/check-disk-space-usage-linux-using-ncdu/
# 可以快速统计磁盘文件的大小, 还可以把结果存下来

agedu
# man agedu 可以看看怎么,  -s -w 这两个参数可以用
# agedu -s /  --cross-fs # scan, 如果不加--cross-fs 不会跨文件系统扫描(间接地限制不会垮硬盘扫描)
# agedu --auth none -f agedu.dat -w --address 0.0.0.0:5432
# - 如果不加 `--auth none` 这边我发现address设置成 0.0.0.0 就会 403 Forbidden, 改成127.0.0.1 然后再端口转发就没问题了
#    - ssh 127.0.0.1 -L 0.0.0.0:48475:127.0.0.1:48474  # 做个端口转发 想让别人也能访问
# 问题
# 曾经一直遇到:  403 Forbidden 的问题无法解决
# - 后来发现其它内置了 authentication 的机制，可以 --auth none 关掉

# END   清理垃圾文件  -----------------------




# BEGIN 其他 ------------------------------


# NFS相关

# https://linoxide.com/linux-how-to/nfs-device-busy/
# 强行umount 再mount
# - 刚刚开机的就出现disk is buzy的问题解决了 (这个常常表现为D进程)
# - 但是之前一直buzy的
# sudo umount -f -l /nfs_data1 && sudo mount -a

# 如何用file cache/cachefilesd 加速nfs
# https://askubuntu.com/questions/4572/how-can-i-cache-nfs-shares-on-a-local-disk 
# https://www.cyberciti.biz/faq/centos-redhat-install-configure-cachefilesd-for-nfs/




# END   其他 ------------------------------
