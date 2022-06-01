import time
from socket import *
from threading import Timer
import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
def time_str_sec(time_element):

    hr_min_sec = time_element.split(':')
    time_in_seconds = int(hr_min_sec[0]) * 3600 + int(hr_min_sec[1]) * 60 + int(hr_min_sec[2])

    return time_in_seconds




def clinetExist(clientIP):
    for client in clientsDict.keys():
        if client == clientIP:
            return True
    return False


def check_lost(clientIP, beat_time):
    last_sent_packet_time = clientsDict[clientIP]
    time_differendce = beat_time - last_sent_packet_time
    if time_differendce > period:
        lost_packets_num = (time_differendce - period) / period
 #       print(f"{lost_packets_num} packet/s got lost")
        list.append(f"{lost_packets_num}") ######################


def check_stopped():
    now_sec = time_str_sec(time.ctime().split()[-2])
    for client in clientsDict.keys():
        time_diff = now_sec - clientsDict[client]
        if time_diff >= timeOut:
            stopped_clients.append(client)
    for client in stopped_clients:
        print(f"Client {client} is disconnected..........................................")###########################
        list2.append(f"Client {client}")

        try:
            del clientsDict[client] #<----------------------------------------------------------*
            print(list2)
        except ValueError:
            continue

    time.sleep(2)

    # for client in clientsDict.keys():
    #     print(f"{client} :  {clientsDict[client]}")###########################


    Timer(timeOut, check_stopped).start()


serverSocket = socket(AF_INET, SOCK_DGRAM)
serverIP = "172.20.10.3"
serverPort = 12345
serverSocket.bind((serverIP, serverPort))

global clientsDict, period, timeOut, stopped_clients,list,list2,json_object
clientsDict = dict()
period = 0.5
timeOut = 5
stopped_clients = []
list=[]
list2=[]



def threadFunc():
    check_stopped()
    while True:
        beat, clientAddress = serverSocket.recvfrom(1024)
        clientIP = clientAddress[0]
        #print(f"Client {clientIP} is connected")
        list.append(clientIP)#######################
        #print(beat.decode())
        list.append(beat.decode())###################
        beat_elements = beat.decode().split()
        seqNum = int(beat_elements[0])
        beat_time = time_str_sec(beat_elements[-2])
        if clinetExist(clientIP):
            check_lost(clientIP, beat_time)
        if(len(list)<3):
            list.append("0")

        clientsDict[clientIP] = beat_time



        my_dict = dict()
        my_dict["connected clint"] = list[0]
        my_dict["beat"] = list[1]
        my_dict["no of lost packets"] = list[2]

        if(len(list2)>0):
            my_dict["disconnected"]=list2[0]
            list2.clear()
        else:
            my_dict["disconnected"] = "non"

        list.clear()

        dlist=[]

        dlist.append(my_dict)

        json_object = json.dumps(dlist, indent=1)

        print(json_object)


th = threading.Thread(target=threadFunc)
th.start()


class Serv(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server) -> None:
        self.flag = False
        super().__init__(request, client_address, server)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers
        self.wfile.write(bytes(json_object, "utf-8"))


httpd = HTTPServer(('127.0.0.1', 8080), Serv)
httpd.serve_forever()
