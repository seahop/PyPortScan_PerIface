#!/bin/bash/python3
import sys
import socket
import ifaddr
import ipaddress
import threading

ipList = []
threads = []
ports = [80, 443]
print_lock = threading.Lock()

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
        
def getNet():
    
    adapters = ifaddr.get_adapters()
            
    for adapter in adapters:
        for ip in adapter.ips:
            if ip.is_IPv4:
                if not ip.ip.startswith("169") or ip.ip.startswith("127"):
                    addr =  ip.ip 
                    netmask = ip.network_prefix
                    host = ipaddress.ip_interface("%s/%s" % (ip.ip, ip.network_prefix))
                    for i in host.network:
                        i = str(i)
                        if not i.endswith(".0"):
                            ipList.append(i)
                    return
                    
def doWork(ip):
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket.setdefaulttimeout(1)
        try:
            result = s.connect_ex((ip,port))
            if result == 0:
                print("Port {} is open on {}".format(port,ip))
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
 
def runThread(ip):
    #calculate number of threads (1 per item in ipList)
    count = 0
    for i in ipList:
        count = count+1
        
    for ip in ipList:
        t = threading.Thread(target=doWork, args= (ip,))
        threads.append(t)

    for i in range(count):
        threads[i].start()

    for i in range(count):
        threads[i].join()
        
def main():
    if len(sys.argv) == 2:
        target = socket.gethostbyname(sys.argv[1])
        byHost(target)
    else:
        getNet()
        runThread(ipList)
     
if __name__ == "__main__":
    main()
