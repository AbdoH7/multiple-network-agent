# import math
# from socket import *
# import time
# startTime = time.time()

# if __name__ == '__main__':
#    target = input('Enter the host to be scanned: ')
#    t_IP = gethostbyname(target)
#    print ('Starting scan on host: ', t_IP)
   
#    for i in range(50, 500):
#       s = socket(AF_INET, SOCK_STREAM)
      
#       conn = s.connect_ex((t_IP, i))
#       if(conn == 0) :
#          print ('Port %d: OPEN' % (i,))
#       s.close()
# print('Time taken:', time.time() - startTime)


# import subprocess
  
# for ping in range(1,30):
#     address = "192.168.1." + str(ping)
#     res = subprocess.call(['ping', '-c', '3', address])
#     if res == 0:
#         print( "ping to", address, "OK")
#     elif res == 2:
#         print("no response from", address)
#     else:
#         print("ping to", address, "failed!")






# from __future__ import print_function

# import types
# from scapy.all import *
# import os

# import ifcfg
# import json

# def arp_scan(interface,ipandsub,verbose=False):
#    packet = Ether(dst = "ff:ff:ff:ff:ff:ff" )/ARP(pdst=ipandsub)
#    ans,unans = srp(packet,timeout=2,iface=interface,verbose=verbose)
#    values=[]
#    for s,r in ans:
#       mac = r.sprintf("%Ether.src%")
#       ip = r.sprintf("%ARP.psrc%")
#       tup = (mac,ip)
#       values.append(tup)
#    return values
	  
# def calculate_network_id(ip_bin,subnet,net_addr):
#    subnet_position = (subnet/8) 
#    position_boundary = (subnet % 8) 
#    calc_octet = ['0','b']
#    if position_boundary > 0:
#       for i in range(2,position_boundary+2):
#          calc_octet.append(ip_bin[subnet_position][i])
#       for i in range(position_boundary+2,10):
#          calc_octet.append('0')
#       ip_bin[subnet_position] = ''.join(calc_octet)
#       if subnet_position < 3:
#          for i in range(subnet_position+1,len(ip_bin)):
#             ip_bin[i] = '0b00000000'
         
#    if (position_boundary == 0 ):
#       for i in range(subnet_position,len(ip_bin)):
#          ip_bin[i] = '0b00000000'
#    for i in range(0,4):
#       net_addr.append(ip_bin[i])
#    return net_addr
   
# def start_scan(verbose=False):
#    default = ifcfg.default_interface()
#    ip = default['inet']
#    ip_list = ip.split(".")
#    ip_bin = []
#    for i in ip_list:
#       each_bin = str(bin(int(i))).lstrip("0b")
#       if len(each_bin) < 10:
#          if len(each_bin) < 8:
#             for j in range(1,(9 - len(each_bin))):
#                each_bin = '0'+str(each_bin)
#          each_bin = '0b'+str(each_bin)
#       ip_bin.append(each_bin)     	  

#    mask = default['netmask']
#    mask = mask.split(".")
#    mask_bin = []
#    subnet = 0
#    net_addr = []
#    for i in mask:
#       bin_eq  = bin(int(i))
#       mask_bin.append(bin_eq)
#       for i in range(2,len(str(bin_eq))):
#          if bin_eq[i] == "1":
#             subnet += 1
#    netid = calculate_network_id(ip_bin,subnet,net_addr)
#    network_id = str(int(netid[0],2))+"."+str(int(netid[1],2))+"."+str(int(netid[2],2))+"."+str(int(netid[3],2))
#    #print(network_id)
#    interface = default['device']
#    ipandsub = network_id+"/"+str(subnet)
#    return arp_scan(interface,ipandsub,verbose)

# def show(devices):
#    for device in devices:
#       print("%s\t%s" % device)

# if __name__ == "__main__":
#    devices = start_scan(verbose=True)
#    show(devices)




##works####  ###platform agnostic###


# linux: [20, 21, 22, 23, 25, 80, 111, 443, 445, 631, 993, 995]
# windows: [135, 137, 138, 139, 445]
# mac: [22, 445, 548, 631]

import socket

def connect(hostname, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    result = sock.connect_ex((hostname, port))
    sock.close()
    return result == 0

for i in range(0,255):
    res = connect("192.168.1."+str(i), 135)
    if res:
        print("Device found at: ", "192.168.1."+str(i) + ":"+str(135))