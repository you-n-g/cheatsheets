#!/bin/bash


# To reliably create a D state process, you can use sshfs to mount a remote directory, then use iptables to block network access, causing processes accessing the mount to enter D state.
# Example:
sudo mkdir -p /mnt/test
sudo chown xiaoyang:xiaoyang /mnt/test
sshfs xiaoyang@ep03.213428.xyz:/home/xiaoyang/ /mnt/test
sudo iptables -A OUTPUT -d ep03.213428.xyz -j DROP
ls /mnt/test/ &  # ls /mnt/test/ will enter D state and can never be killed

# Cleanup:
sudo iptables -D OUTPUT -d ep03.213428.xyz -j DROP
fusermount -u /mnt/test


# If you don't use timeout, there is still no reliable user-space method to stop (kill) a process stuck in D state; neither `kill` nor `kill -9` will work. You must resolve the underlying I/O (e.g., restore network connectivity, unmount the filesystem, or reboot the system) to allow the process to terminate. D state processes are uninterruptible by design.
