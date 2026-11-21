from socket import *
import sys,json

import packet, time

import log

NUM_PROBES = 25
DEFAULT_PROBE_INTERVAL = 1

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
    probeInterval = float(sys.argv[5]) if len(sys.argv) > 5 else DEFAULT_PROBE_INTERVAL

    failureTime = None
    recoveryTime = None

    print(f"Sending packet to {neighborPort}")
    print(f"Probe interval: {probeInterval} seconds")

    for i in range(NUM_PROBES):
        probeMsg = packet.make(addressName, otherHostName, 'probe', packet.HOP_LIMIT, i, 'SLU CS rules!!!')
        encodedProbeMsg = packet.encode(probeMsg)

        sec = time.monotonic()
        hostSocket.sendto(encodedProbeMsg, (ip, neighborPort))
        log.write(hostName, 'send', probeMsg, neighborPort, 'no issue, probe sent')

        try:
            data, addr = hostSocket.recvfrom(2048)
        except timeout:
            log.write(hostName, 'timeout', probeMsg, None, 'no echo')
            timeouts += 1

            if failureTime is None:
                failureTime = time.monotonic()
                print("No echo received. Waiting for successful echo.")

            time.sleep(probeInterval)
            continue

        decoded = packet.decode(data)

        if decoded is None:
            log.write(hostName, 'drop', None, None, 'invalid packet')
            time.sleep(probeInterval)
            continue

        if (decoded['type'] == 'echo'
                and decoded['id'] == probeMsg['id']
                and decoded['src'] == otherHostName
                and decoded['dest'] == addressName):

            matched += 1
            log.write(hostName, 'receive', decoded, neighborPort,
                      f"echo received in {(time.monotonic() - sec) * 1000} ms")

            if failureTime is not None and recoveryTime is None:
                recoveryTime = time.monotonic()
                elapsed = recoveryTime - failureTime
                print(f"Alternate path recovery time: {elapsed:.3f} seconds")

        time.sleep(probeInterval)

    print(f"{NUM_PROBES} sent", f"{matched} matched", f"{timeouts} timed out")

    if failureTime is not None and recoveryTime is None:
        print("Alternate path recovery was not detected.")
    elif failureTime is None:
        print("No failure was detected during probing.")

elif action == 'listen':
    print(f"Listening packet from {neighborPort}")
    while True:
        data, addr = hostSocket.recvfrom(2048)
        decoded = packet.decode(data)

        if decoded is None:
            log.write(hostName, 'drop', None, None, 'invalid packet')
            continue

        log.write(hostName, 'receive', decoded, None, 'no issue, packet received')

        if decoded['type'] == 'probe' and decoded['dest'] == addressName:
            echoMsg = packet.make(addressName, decoded['src'], 'echo',
                                  packet.HOP_LIMIT, decoded['id'], decoded['data'])
            encodedEchoMsg = packet.encode(echoMsg)
            hostSocket.sendto(encodedEchoMsg, (ip, neighborPort))
            log.write(hostName, 'send', echoMsg, neighborPort, 'no issue, echo sent')

else:
    print("Wrong action")
    exit(1)
