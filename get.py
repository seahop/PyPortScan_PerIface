#!/bin/bash/python3
import sys
import socket
import ifaddr
import ipaddress

ports = (80, 443)

def byHost( target ):
    try:
        for port in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            result = s.connect_ex((target,port))
            if result == 0:
                print("Port {} is open on {}".format(port,target))
            s.close()

    except KeyboardInterrupt:
        print("\n Exiting Program !!!!")
        sys.exit()
    except socket.gaierror:
        print("\n Hostname Could Not Be Resolved !!!!")
        sys.exit()
    except socket.error:
        print("\ Server not responding !!!!")
        sys.exit()
    return
        
def byNet():
    
    adapters = ifaddr.get_adapters()
            
    for adapter in adapters:
        for ip in adapter.ips:
            if ip.is_IPv4:
                if not ip.ip.startswith("169") or ip.ip.startswith("127"):
                    addr =  ip.ip 
                    netmask = ip.network_prefix
                    host = ipaddress.ip_interface("%s/%s" % (ip.ip, ip.network_prefix))
                    try:
                        for i in host.network:
                            i = str(i)
                            #print(i)
                            if not i.endswith(".0"):
                                print(i)
                                for port in ports:
                                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                    socket.setdefaulttimeout(1)
                                    result = s.connect_ex((i,port))
                                    if result == 0:
                                        print("Port {} is open on {}".format(port,i))
                                        s.close()
                            
                    except KeyboardInterrupt:
                        print("\n Exiting Program !!!!")
                        sys.exit()
                    except socket.gaierror:
                        print("\n Hostname Could Not Be Resolved !!!!")
                        sys.exit()
                    except socket.error:
                        print("\ Server not responding !!!!")
                        sys.exit()
                    return
 
    
    

# Defining a target
if len(sys.argv) == 2:
    target = socket.gethostbyname(sys.argv[1])
    byHost(target)
else:
    byNet()
