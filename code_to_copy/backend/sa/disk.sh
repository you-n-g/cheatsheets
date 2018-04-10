#!/usr/bin/env bash




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
mkfs.ext4 /dev/xvdb1 # 注意是分区
mkswap /dev/xvdb1 # swapon /dev/xvdb1 来挂载分区


# 3) /etc/fstab
# man fstab 中有详细的说明
# 分区 路径 文件系统 挂载参数(普通的都用defaults) 是否需要备份(一般是不需要,用0)  自检顺序(0不需自检，/应该为1，其他分区为2)
/dev/xvdb1 /data/                   ext4    defaults        0 2
/dev/xvdb2 none            swap    sw              0       0
# mount -a 会自动挂载fstab中的东西，  可以以此检测



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
