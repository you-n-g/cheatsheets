#!/usr/bin/env bash


# boot the vm
nova boot <vm_name> --image <image_name> --flavor <flavor_id>

# download vm image and create image
# the images are stored in /data/glance/images/
glance image-create --name <image_name> --disk-format=<same_as_image-list> --container-format=bare --file <image-file>




# restart all the openstack service
for svc in api conductor scheduler compute network   cert ; do service openstack-nova-$svc restart; done

