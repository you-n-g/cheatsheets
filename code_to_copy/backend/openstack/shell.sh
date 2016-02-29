#!/usr/bin/env bash

# 
nova hypervisor-[list|servers|show|stats|uptime]
# 用于看具体的compute节点上的hypervisor 的各种详细信息

# boot the vm
nova boot <vm_name> --image <image_name> --flavor <flavor_id>

# download vm image and create image
# the images are stored in /data/glance/images/
glance image-create --name <image_name> --disk-format=<same_as_image-list> --container-format=bare --file <image-file>




# restart all the openstack service
for svc in api conductor scheduler compute network cert; do service openstack-nova-$svc restart; done

