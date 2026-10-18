from socket import *
import sys,json

# command line
configType = sys.argv[1]
routerName = sys.argv[2]
config = json.load(open(f'{configType}.json'))
routerInfo = config[routerName]

#print(routerInfo)


port = routerInfo['local_port']
serverSocket = socket(AF_INET, SOCK_DGRAM)

ip = routerInfo['ip']
serverSocket.bind((ip, port))

print(f"Server ready for receiving on port {port}")

while True:
    message, address = serverSocket.recvfrom(2048)
    print(message)
    # temp fixed next hop
    serverSocket.sendto(message, (ip, 2222))