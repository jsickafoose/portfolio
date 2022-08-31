from ece121 import Protocol
import time
import datetime

def MonitorPrint(inBytes):
	Message = inBytes[1:]
	ID = inBytes[0]
	try:
		IDString = Protocol.MessageIDs(ID).name
	except ValueError:
		IDString = "Invalid ID ({})".format(ID)
	# print(IDString)
	try:
		Message = Message.decode('ascii')
	except UnicodeError:
		pass
	print("{}\t{}\t{}".format(datetime.datetime.now(), IDString, Message))
	return

def DisconnectHandler(inException):
	print(inException)
	while True:
		time.sleep(.1)
		if prot.Connect():
			print("Connected to {}".format(prot.Port))
			break
	return

print("Current Serial Ports", Protocol.Protocol.listSerialPorts())
prot = Protocol.Protocol()

for enum in Protocol.MessageIDs:
	prot.registerMessageHandler(enum, MonitorPrint)
# prot.registerHandler(Protocol.MessageIDs.ID_DEBUG, MonitorPrint)
prot.registerErrorHandler(DisconnectHandler)

if not prot.activeConnection:
	print("No Serial Port Found")
	while True:
		time.sleep(.1)
		if prot.Connect():
			print("Connected to {}".format(prot.Port))
			break

while True:
	time.sleep(1)
