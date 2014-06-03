#!/usr/bin/env bash

# 0) 查看硬盘
fdisk -l

# 1) 先分区
fdisk  /dev/sda #注意是对整个disk而不是分区
# 常用命令
p # 打印分区表
n # 新建分区表
w # 写入分区表

# 2) 创建文件系统
mkfs.ext4 /dev/xvdb1 # 注意是分区


# 3) /etc/fstab
# man fstab 中有详细的说明
# 分区 路径 文件系统 挂载参数(普通的都用defaults) 是否需要备份(一般是不需要,用0)  自检顺序(0不需自检，/应该为1，其他分区为2)
/dev/xvdb1 /data/                   ext4    defaults        0 2
# mount -a 会自动挂载fstab中的东西，  可以以此检测



# 分区扩展 
# 删除该分区, 然后再创建同一起始扇区， 任意结束扇区的分区， 数据会被保留
# 感觉很危险， 不知道可不可信 http://litwol.com/content/fdisk-resizegrow-physical-partition-without-losing-data-linodecom
