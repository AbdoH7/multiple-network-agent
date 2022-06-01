import json 
from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import os
import _thread
import subprocess    




json_object=[]
list=[]


def ping(ip):  
    os.system('ping -c 2  '+ip)

for i in range (0,255):
    _thread.start_new_thread(ping,("192.168.1."+str(i),))

time.sleep(30)
output = subprocess.check_output('arp -a', shell=True)
output=str(output)
output=output.strip("b'")
output=output.split("\\n")
for i in range (len(output)):
    output[i]=output[i].split(" ")

output.pop(len(output)-1)

for i in range (len(output)):
    output[i].pop(2)
    output[i].pop(3)
    output[i].pop(3)
    output[i].pop(3)

for i in range(len(output)):
    my_dict = dict()
    for j,value in enumerate(output[i]):
        if(j==0):
            my_dict["Host_name"]= value
        elif(j==1):
            value=value.strip("(")
            value=value.strip(")")
            my_dict["ip_address"]=value
        else:
            my_dict["mac_address"]=value
        
    list.append(my_dict)

json_object=json.dumps(list,indent=1)
print(json_object)
class Serv(BaseHTTPRequestHandler): 

  def do_GET(self):

    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.send_header('Access-Control-Allow-Origin','*')
    self.end_headers
    self.wfile.write(bytes(json_object,"utf-8"))
httpd = HTTPServer(('127.0.0.1', 8099), Serv)
httpd.serve_forever()
