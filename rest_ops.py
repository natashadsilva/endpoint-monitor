# Licensed Materials - Property of IBM
# Copyright IBM Corp. 2019

import requests
import endpoint_monitor

def server_url(server):
    return '%s://%s:%s/' % (server.proto, server.ip, server.port)


# Currently unused
def find_contexts(server, url, client_cert):
    oppaths=set()
    contexts=set()
    exposed_ports = None
    ports_url = url + 'ports/info'
    ports = requests.get(ports_url, cert=client_cert, verify=False).json()
    if 'exposedPorts' in ports:
        exposed_ports = ports['exposedPorts']
        for port in exposed_ports:
            cps = port['contextPaths']
            for id_ in cps:
                cp = cps[id_].replace('\\', '')
                scp = cp.split('/')
                contexts.add(scp[1])
                oppaths.add(scp[1]+'/'+scp[2])

    return contexts, oppaths, exposed_ports


def fill_in_details(endjob, client_cert):
    for server in endjob.servers:
        url = server_url(server)
        contexts, paths = find_contexts(server, url, client_cert)
        endjob.server_details[server] = endpoint_monitor.ServerDetail(url, contexts, paths, exposed_ports)
        print('Server', server)
        print('ServerDetail', endjob.server_details[server])
