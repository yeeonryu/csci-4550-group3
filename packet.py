import json

MAX_SIZE = 1200


def make(src, dest, packetType, hopLimit, packetId, data):
   return {
    'src': src,
    'dest': dest,
    'type': packetType,
    'hopLimit': hopLimit,
    'id': packetId,
    'data': data,
    }

def encode(packet):
    encodedPacket = json.dumps(packet).encode()
    return encodedPacket if len(encodedPacket) <= MAX_SIZE else None

def decode(ePacket):
    decodedPacket = json.loads(ePacket.decode())
    return decodedPacket if len(ePacket) <= MAX_SIZE else None


# test
if __name__ == "__main__":
    testPacket = make('hostOne','hostTwo','probe',1,1,'SLU CS rules!!!')
    encodedTest = encode(testPacket)
    decodedTest = decode(encodedTest)
    print(testPacket['data'])
    print(decodedTest['data'])