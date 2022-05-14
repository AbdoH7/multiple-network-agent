
import os
import _thread
import time


def ping(ip):  
    os.system('ping -c 1 '+ip)
    


for i in range (0,255):
    _thread.start_new_thread(ping,("192.168.1."+str(i),))
    

time.sleep(20)
os.system('arp')
