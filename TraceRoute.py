from posixpath import split
import time
import subprocess
import json
from socket import *
from http.server import HTTPServer , BaseHTTPRequestHandler

list=[]
Websites={"google.com","Apple.com"}
for p in Websites:
   TraceRoute= subprocess.getoutput(f"traceroute {p}").split("\n")
   last=TraceRoute[len(TraceRoute)-1].split()
   #print(TraceRoute[0])
   HopNum=last[0]
   time=[]
   for i in last:
    if(i.endswith("ms")):
     time.append(i)
   time=[s.replace("ms", "") for s in time]
   Average = 0
   for i in time: 
    Average= Average+float(i)
   Average=Average/3.0
   data={
        "dstName":p,
        "HopNum":HopNum,
        "AverageTime":Average
     }
   list.append(data)
json_object=json.dumps(list)     
print(json_object)

class Serv(BaseHTTPRequestHandler):
     def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Content-type','application/json')
        self.end_headers
        self.wfile.write(bytes(json_object,"utf-8"))
httpd= HTTPServer(('192.168.43.25',8100),Serv)

httpd.serve_forever()
