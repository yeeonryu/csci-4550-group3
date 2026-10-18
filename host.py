from socket import *
import sys,json

import packet, time

# command line
configType = sys.argv[1]
hostName = sys.argv[2]
action = sys.argv[3]
config = json.load(open(f'{configType}.json'))
hostInfo = config[hostName]

#print(hostInfo)


port = hostInfo['local_port']
hostSocket = socket(AF_INET, SOCK_DGRAM)

ip = hostInfo['ip']
hostSocket.bind((ip, port))

neighborPort = hostInfo['neighbor_ports'][0]
addressName = hostInfo['address_name']

if action == 'send':
    otherHostName = sys.argv[4]
    print(f"Sending packet to {neighborPort}")
    probeMsg = packet.make(addressName, otherHostName, 'probe', packet.HOP_LIMIT, 1, 'SLU CS rules!!!')
    encodedProbeMsg = packet.encode(probeMsg)
    sec = time.monotonic()
    hostSocket.sendto(encodedProbeMsg, (ip, neighborPort))
    data, addr = hostSocket.recvfrom(2048)
    decoded = packet.decode(data)
    if decoded['type'] == 'echo' and decoded['id'] == probeMsg['id']:
        print(f"Echo received from {decoded['src']} in {(time.monotonic() - sec) * 1000} ms")

elif action == 'listen':
    print(f"Listening packet from {neighborPort}")
    while True:
        data, addr = hostSocket.recvfrom(2048)
        decoded = packet.decode(data)
        print(decoded)
        if decoded['type'] == 'probe'and decoded['dest'] == addressName:
            echoMsg =packet.make(addressName, decoded['src'], 'echo', packet.HOP_LIMIT, decoded['id'], decoded['data'])
            encodedEchoMsg = packet.encode(echoMsg)
            hostSocket.sendto(encodedEchoMsg, (ip, neighborPort))
else:
    print("Wrong action")
    exit(1)