#! /bin/bash
source /home/stack/overcloudrc
set -x

if ! neutron net-list|grep -q ext_net ; then
    neutron net-create ext_net --router:external
    neutron subnet-create ext_net 192.168.24.0/24 --name ext_net_sub \
    --enable-dhcp=False --allocation-pool start=192.168.24.100,end=192.168.24.230 \
    --dns-nameserver 192.168.23.1
fi

if ! ls CentOS-7-x86_64-GenericCloud.qcow2 ; then
   curl -O http://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud.qcow2
   openstack image create --file CentOS-7-x86_64-GenericCloud.qcow2 centos
fi

if ! openstack keypair list|grep -q my_key ; then
    openstack keypair create --public-key /home/stack/.ssh/id_rsa.pub my_key
fi

if ! openstack flavor list|grep -q my.tiny.vnf ; then
    openstack flavor create --ram 512 --disk 10 --vcpus 1 m1.tiny.vnf
fi

# openstack stack create -t --file vnfm.yaml vnfm 
