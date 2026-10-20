from socket import *
import sys,json
import packet

# if the user doesn't supply enough arguments
if len(sys.argv) != 3:
    print("Usage: python router.py <configType> <routerName>")
    sys.exit(1)

# command line
configType = sys.argv[1]
routerName = sys.argv[2]

# Handle invalid configuration files
try:
    config = json.load(open(f'{configType}.json'))
except FileNotFoundError:
    print(f"Error: Configuration file '{configType}.json' not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Configuration file '{configType}.json' contains invalid JSON.")
    sys.exit(1)

# Check whether the router exists
if routerName not in config:
    print(f"Error: Router '{routerName}' not found in configuration.")
    sys.exit(1)

routerInfo = config[routerName]

# Check if the forwarding table exists
if 'table' not in routerInfo:
    print(f"Error: Forwarding table missing for '{routerName}',")
    sys.exit(1)

if not isinstance(routerInfo['table'], dict):
    print(f"Error: Invalid forwarding table for '{routerName}',")
    sys.exit(1)

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