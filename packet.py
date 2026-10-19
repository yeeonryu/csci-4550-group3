
import json

MAX_SIZE = 1200
HOP_LIMIT = 8

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
    if not validate(packet):
        return None

    try:
        encodedPacket = json.dumps(packet).encode()
        return encodedPacket if len(encodedPacket) <= MAX_SIZE else None
    except (TypeError, ValueError):
        return None

def decode(ePacket):
    if not isinstance(ePacket, bytes):
        return None

    if len(ePacket) > MAX_SIZE:
        return None

    try:
        decodedPacket = json.loads(ePacket.decode())
        return decodedPacket if validate(decodedPacket) else None
    except (ValueError, UnicodeDecodeError):
        return None

def validate(packet):
    if not isinstance(packet, dict):
        return False

    required = {'src', 'dest', 'type', 'hopLimit', 'id', 'data'}

    if not required.issubset(packet.keys()):
        return False

    if not isinstance(packet['src'], str) or not packet['src']:
        return False

    if not isinstance(packet['dest'], str) or not packet['dest']:
        return False

    if packet['type'] not in ('probe', 'echo'):
        return False

    if type(packet['hopLimit']) is not int:
        return False

    if not 0 <= packet['hopLimit'] <= HOP_LIMIT:
        return False

    if type(packet['id']) is not int or packet['id'] < 0:
        return False

    if not isinstance(packet['data'], str):
        return False

    return True


# test
if __name__ == "__main__":
    testPacket = make('hostOne', 'hostTwo', 'probe', 1, 1, 'SLU CS rules!!!')

    encodedTest = encode(testPacket)
    decodedTest = decode(encodedTest)

    print(testPacket['data'])
    print(decodedTest['data'])
    print(validate(decodedTest))

    # Invalid packet
    print(encode({'src': 'hostOne'}))

    # Invalid packet type
    invalidPacket = make('hostOne', 'hostTwo', 'invalid', 1, 1, 'Hello')
    print(validate(invalidPacket))

    largePacket = make('hostOne', 'hostTwo', 'probe', 1, 1, 'A' * 1200)
    print(encode(largePacket))

    print(decode(b'{invalid json}'))
