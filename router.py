from socket import *
import sys,json
import packet
import random

import log

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

lossRate = routerInfo.get('loss_rate', 0.0)
seed = routerInfo.get('seed', 1)
lossNextHop = routerInfo.get('next_hop', None)
dropId = routerInfo.get('drop_id', None)

randomSeed = random.Random(seed)

# Check if the forwarding table exists
if 'table' not in routerInfo:
    print(f"Error: Forwarding table missing for '{routerName}',")
    sys.exit(1)

if not isinstance(routerInfo['table'], dict):
    print(f"Error: Invalid forwarding table for '{routerName}',")
    sys.exit(1)

# Check whether neighbor ports exist
if 'neighbor_ports' not in routerInfo:
    print(f"Error: Neighbor ports missing for '{routerName}'")
    sys.exit(1)

# Check whether neighbor ports are stored as a list
if not isinstance(routerInfo['neighbor_ports'], list):
    print(f"Error: Invalid neighbor ports for '{routerName}'")
    sys.exit(1)

# Check that each forwarding-table entry points to a neighbor
for destination, nextHop in routerInfo['table'].items():
    if nextHop not in routerInfo['neighbor_ports']:
        print(f"Error: Invalid next hop {nextHop} for destination '{destination}'")
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
        log.write(routerName, 'drop', None, None, 'invalid packet')
        continue
    decoded['hopLimit'] -= 1
    dest = decoded['dest']
    if decoded['hopLimit'] < 1:
        log.write(routerName, 'drop', decoded, None, 'hop limit passed')
        continue
    if dest not in routerInfo['table']:
        log.write(routerName, 'drop', decoded, None, 'destination not in forwarding table')        
        continue
    nextHop = routerInfo['table'][dest]
    if nextHop not in routerInfo['neighbor_ports']:
        log.write(routerName, 'drop', decoded, nextHop, 'not a neighbor port')
        continue
    else:
        if nextHop == lossNextHop:
            if dropId is not None and decoded['id'] == dropId:
                log.write(routerName, 'drop', decoded, nextHop, 'drop is forced')
                continue
            if randomSeed.random() < lossRate:
                log.write(routerName, 'drop', decoded, nextHop, 'drop because of loss rate triggered')
                continue
        encoded = packet.encode(decoded)
        routerSocket.sendto(encoded, (ip, nextHop))
        log.write(routerName, 'forward', decoded, nextHop, 'no issue with forward')
