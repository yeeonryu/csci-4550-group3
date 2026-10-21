import time, os

def write(devName, event, packetDict, nextHop, reason):
    if packetDict is None:
        packetDict = {}
    with open('log.txt', 'a') as f:
        logged = f"{devName}, {event}, {packetDict.get('src','')}, {packetDict.get('dest','')}, {packetDict.get('type', '')}, {packetDict.get('hopLimit','')}, {packetDict.get('id','')}, {nextHop}, {reason}, {time.time()}, {os.environ.get('RUN_ID', 'manual')}\n"
        print(logged)
        f.write(logged)
        f.close()

if __name__ == "__main__":
    import packet
    test = packet.make('hostOne', 'hostTwo', 'probe', packet.HOP_LIMIT, 1, 'SLU CS rules!!!')
    write('hostOne', 'send', test, 3333, 'test')
    write('hostOne', 'receive', test, 3333, 'test')
    write('hostOne', 'timeout', None, None, 'no echo')