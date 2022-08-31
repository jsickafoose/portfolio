from ece121 import Protocol
import sys
import argparse



parser = argparse.ArgumentParser()
parser.add_argument("stringToEncode", help="String to encode within a debug message")

args = parser.parse_args()

rawpayload = args.stringToEncode
payload = rawpayload.encode("ascii")
print("Given Payload: {}".format(rawpayload))
portInstance = Protocol.Protocol()

message = bytearray()
message += Protocol.HEADER
payload  = Protocol.MessageIDs.ID_DEBUG.value.to_bytes(1, byteorder='big')+payload
message += (len(payload)).to_bytes(1, byteorder='big')
message += payload


message += Protocol.TAIL
checksum = portInstance.calcChecksum(payload)
message += checksum.to_bytes(1, byteorder='big')
message += bytes("\r\n".encode('ascii'))

# print(message)
print("Raw Hex: 0X{}".format(message.hex().upper()))
print("C Array: {{{}}}".format(", ".join([str(x) for x in message])))

