from socket import *
import sys,json
import packet

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
    decoded = packet.decode(message)
    if not packet.validate(decoded):
        print("Packet is not valid, dropping the packet")
        continue
    decoded['hopLimit'] -= 1
    dest = decoded['dest']
    if decoded['hopLimit'] < 1:
        print("Hop limit is ", decoded['hopLimit'], ", dropping the packet")
        continue
    nextHop = routerInfo['table'][dest]
    if nextHop not in routerInfo['neighbor_ports']:
        print("Next hop is not in the neighbor ports, dropping the packet")
        continue
    else:
        encoded = packet.encode(decoded)
        routerSocket.sendto(encoded, (ip, nextHop))
        print(dest, nextHop)