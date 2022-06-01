import http
import subprocess
from socket import *
from urllib import request
import json
from http.server import HTTPServer , BaseHTTPRequestHandler


# output = subprocess.check_output("ss -udp -t -O", shell = True)
# output = output.decode()
# lines = output.split("\n")
# info_of_ports = []
# for line in lines:
#     line = line.split()
#     if line.__len__() == 7:
#         if line[4].__contains__("192.168.1."):
#             port = line[4].split(":")[1]
#             dest_ip = line[5].split(":")[0]
#             port_info = {'port': port, 'dest_ip':dest_ip}
#             info_of_ports.append(port_info)

# json_object = json.dumps(info_of_ports)
# print(json_object)

# for info in info_of_ports:
#     print(info)

# print(info_of_ports.__len__())
# serverport = 2001
# serverSocket = socket(AF_INET, SOCK_DGRAM)
# serverSocket.bind(('172.20.10.3',serverport))
# print("The port scanner is ready to send")

# ip = 0
# print(f"{(info_of_ports[ip])['port']}:{(info_of_ports[ip])['dest_ip']}")
# while True:
#     msg,requester = serverSocket.recvfrom(1024)
#     print(msg.decode())
#     if ip == info_of_ports.__len__() - 1:
#         serverSocket.sendto(bytes("end".encode("utf-8")),requester)
#         serverSocket.close()
#         break
#     if msg.decode() == 'request':
#         msg_to_be_sent = f"{(info_of_ports[ip])['port']}:{(info_of_ports[ip])['dest_ip']}"
#         serverSocket.sendto(bytes(msg_to_be_sent.encode("utf-8")), requester)
#     elif msg.decode() == 'end':
#         serverSocket.close()
#         break
#     ip += 1

print("we are out of the socket loop")


class Serv(BaseHTTPRequestHandler):
    def do_GET(self):
        output = subprocess.check_output("ss -udp -t -O", shell = True)
        output = output.decode()
        lines = output.split("\n")
        info_of_ports = []
        for line in lines:
            line = line.split()
            if line.__len__() == 7:
                if line[4].__contains__("172.20.10."):
                    port = line[4].split(":")[1]
                    dest_ip = line[5].split(":")[0]
                    port_info = {'port': port, 'dest_ip':dest_ip}
                    info_of_ports.append(port_info)

        json_object = json.dumps(info_of_ports)
        print(json_object)

        for info in info_of_ports:
            print(info)

        print(info_of_ports.__len__())
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Content-type','application/json')
        self.end_headers
        self.wfile.write(bytes(json_object,"utf-8"))
httpd= HTTPServer(('172.20.10.4',8080),Serv)

httpd.serve_forever()    