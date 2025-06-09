#!/bin/sh
cd ~/tmp/test_overlay/
mkdir -p ./lower ./upper ./work ./merged

echo we are here > ./merged/original
ls ./merged

# Assuming /lower contains the base files
# /upper is where changes will be written
# /work is required for overlay filesystem operations
sudo mount -t overlay overlay -o lowerdir=./lower,upperdir=./upper,workdir=./work ./merged/

ls ./merged

sudo umount ./merged

ls ./merged
