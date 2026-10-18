from socket import *
import sys,json

# command line
configType = sys.argv[1]
routerName = sys.argv[2]
config = json.load(open(f'{configType}.json'))
routerInfo = config[routerName]

#print(routerInfo)


port = routerInfo['local_port']
routerSocket = socket(AF_INET, SOCK_DGRAM)

ip = routerInfo['ip']
routerSocket.bind((ip, port))

print(f"Server ready for receiving on port {port}")

while True:
    message, address = routerSocket.recvfrom(2048)
    print(message)
    # temp fixed next hop
    routerSocket.sendto(message, (ip, 2222))