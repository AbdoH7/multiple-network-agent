from socket import *
import time
import random
serverIP = "172.20.10.2"
serverPort = 12345
clientSocket = socket(AF_INET, SOCK_DGRAM)

period = 0.5
i = 0
while True:
	time.sleep(period)
	beat = f"{i}  {time.ctime()}"
	i += 1
	print(beat)
	rand = random.randint(0,10)
	print(rand)
	if rand < 4:
		continue
	print("packet sent")
	clientSocket.sendto(beat.encode(), (serverIP, serverPort))