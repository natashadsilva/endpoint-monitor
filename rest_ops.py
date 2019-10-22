# Licensed Materials - Property of IBM
# Copyright IBM Corp. 2019

import requests
import endpoint_monitor

def server_url(server):
    return '%s://%s:%s/' % (server.proto, server.ip, server.port)


# Currently unused
def find_contexts(server):
    if proto != 'http':
        return set(), set()
    oppaths=set()
    contexts=set()
    ports_url = server_url(server) + 'ports/info'
    ports = requests.get(ports_url, verify=False).json()
    if 'exposedPorts' in ports:
        for port in ports['exposedPorts']:
            cps = port['contextPaths']
            for id_ in cps:
                cp = cps[id_].replace('\\', '')
                scp = cp.split('/')
                contexts.add(scp[1])
                oppaths.add(scp[1]+'/'+scp[2])

    return oppaths, contexts


def fill_in_details(endjob):
    for server in endjob.servers:
        url = server_url(server)
        contexts = set()
        endjob.server_details[server] = endpoint_monitor.ServerDetail(url, contexts)
