#! /bin/python

import socket
import sys

from keystoneauth1 import loading
from keystoneauth1 import session
from novaclient import client as nova_client
from heatclient import client as heat_client

HOSTNAME = socket.gethostname()

OS_USERNAME = "admin"
OS_PASSWORD = "9BhbZq92WEQ7sPr6AhmTm6pQv"
OS_PROJECT_NAME = "admin"
OS_AUTH_URL = "http://192.168.24.8:5000/v2.0"
NOVA_VERSION = "2"
HEAT_VERSION = '2'

data = {}.fromkeys(['vnfm_name', 'vnfm_floating_ip', 'vnf_name'
                   'vnfcs', 'vnfc_mgmt_ip', 'vnfc_host'])

loader = loading.get_plugin_loader('password')
auth = loader.load_from_options(auth_url=OS_AUTH_URL,
                                username=OS_USERNAME,
                                password=OS_PASSWORD,
                                project_name=OS_PROJECT_NAME)
sess = session.Session(auth=auth)
nova = nova_client.Client(NOVA_VERSION, session=sess)
servers = nova.servers.list()
server = nova.servers.find(name=HOSTNAME)

floating_ip = nova.floating_ips.find(instance_id=server.id)

data['vnfm_name'] = server.human_id
data['vnfm_floating_ip'] = floating_ip.ip
data['vnf_name'] = sys.argv[0]
#data['vnf_name'] = 'vnf_a'
data['vnfcs'] = {}
data['vnfc_mgmt_ip'] = {}
data['vnfc_host'] = {}

heat = heat_client.Client('1', session=sess)
for i in heat.stacks.list():
    if i.stack_name == data['vnf_name']:
        for r in heat.resources.list(i.id):
            if (r.resource_type == 'OS::Nova::Server'):
                data['vnfcs'][r.resource_name] = r.physical_resource_id
                 
                server = nova.servers.find(id = r.physical_resource_id) 
                data['vnfc_mgmt_ip'][r.resource_name] = server.networks['mgmt_net']
                data['vnfc_host'][r.resource_name]  = \
                    server.__dict__['OS-EXT-SRV-ATTR:host'].split('.')[0]
print data
