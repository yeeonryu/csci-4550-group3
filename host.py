from socket import *
import sys,json

import packet, time

NUM_PROBES = 25

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
    matched = 0
    timeouts = 0
    hostSocket.settimeout(1)

    otherHostName = sys.argv[4]
    print(f"Sending packet to {neighborPort}")
    for i in range(NUM_PROBES):
        probeMsg = packet.make(addressName, otherHostName, 'probe', packet.HOP_LIMIT, i, 'SLU CS rules!!!')
        encodedProbeMsg = packet.encode(probeMsg)
        sec = time.monotonic()
        hostSocket.sendto(encodedProbeMsg, (ip, neighborPort))
        try:
            data, addr = hostSocket.recvfrom(2048)
        except timeout:
            timeouts += 1
            continue
        decoded = packet.decode(data)
        if decoded == None:
            continue
        if decoded['type'] == 'echo' and decoded['id'] == probeMsg['id']:
            matched += 1
            print(f"Echo received from {decoded['src']} in {(time.monotonic() - sec) * 1000} ms")
    print(f"{NUM_PROBES}sent",f"{matched} matched", f" {timeouts} timed out")

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