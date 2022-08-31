from builtins import int

import serial
import threading
import enum
import queue
import serial.tools.list_ports
import functools
import time
from ece121.Protocol.MessageIDs import MessageIDs as MessageIDs

HEADER = (204).to_bytes(1, byteorder='big')
TAIL = (185).to_bytes(1, byteorder='big')
RAWQUEUESIZE = 2048

class ProtocolStates(enum.Enum):
	# Init = enum.auto()
	HeaderWait = enum.auto()
	LenGrab = enum.auto()
	RecordingPayload = enum.auto()
	TailCheck = enum.auto()
	ParseMessage = enum.auto()



class Protocol(object):
	def __init__(self, Port = None, BaudRate = 115200):


		# store the port info in instance variables
		self.Port = Port
		self.BaudRate = BaudRate

		# set up the dictionary for callbacks
		self.callBackDict = dict()

		# set up the list for error handlers
		self.errorBackList = list()

		# set up the list for packet decoding errors
		self.packetDecodeErrorsBack = list()

		# set up list for outgoing messages
		self.outMessageCallBacks = list()

		# set up queue for outgoing serial as the serial write is blocking
		self.outputQueue = queue.Queue()

		# count packets
		self.packetCountReceiving = 0
		self.packetCountSending = 0

		# connect to the port but first set the activeFlag and create a ref to the port
		self.activeConnection = False
		self.serialPort = None
		self.Connect()

		# clear the buffer
		if self.activeConnection:
			self.serialPort.reset_input_buffer()
			self.serialPort.reset_output_buffer()

		# set up the threaded input buffer
		self.protoclThread = threading.Thread(target=self.handleProtocol, name='ProtocolHandler')
		self.protoclThread.daemon = True
		self.protoclThread.start()

		# set up the threaded output buffer
		self.outputThread = threading.Thread(target=self.handleOutGoing, name='outgoingQueue')
		self.outputThread.daemon = True
		self.outputThread.start()

		return

	@staticmethod
	def listSerialPorts():
		return [potPort.device for potPort in serial.tools.list_ports.comports()]

	def Connect(self):
		# we will handle the no port case here
		if self.Port is None:
			for potPort in serial.tools.list_ports.comports():
				if potPort.device == 'COM1':
					continue
				self.Port = potPort.device
		if self.Port is None:
			self.activeConnection = False
			return False
		else:
			try:
				# open the serial port
				self.serialPort = serial.Serial()
				self.serialPort.baudrate = self.BaudRate
				self.serialPort.port = self.Port
				self.serialPort.dtr = None
				self.serialPort.open()
				self.activeConnection = True
				return True
			except serial.serialutil.SerialException:
				pass
		return False

	def Disconnect(self):
		if self.activeConnection:
			self.activeConnection = False
			self.serialPort.close()
			return True
		else:
			return False

	def registerMessageHandler(self, messageID, functionPointer):
		if type(messageID) is not MessageIDs:
			return False
		if messageID.value in self.callBackDict:
			self.callBackDict[messageID.value].append(functionPointer)
		else:
			self.callBackDict[messageID.value] = [functionPointer]
		return True

	def deregisterMessageHandler(self, messageID, functionPointer):
		if type(messageID) is not MessageIDs:
			return False
		if messageID.value in self.callBackDict:
			self.callBackDict[messageID.value].remove(functionPointer)
		return True

	def registerOutGoingMessageHandler(self, functionPointer):
		"""gets a callback on outgoing messages, this is for all messages, up to application to filter"""
		self.outMessageCallBacks.append(functionPointer)

	def registerErrorHandler(self, functionPointer):
		"""this is for errors in the serial stream, not in the packets"""
		self.errorBackList.append(functionPointer)
		return

	def registerPacketError(self, functionPointer):
		self.packetDecodeErrorsBack.append(functionPointer)
		return

	def handleProtocol(self):
		"""This is the threaded instance that actually handles the protocol"""
		rawQueue = list()
		currentState = ProtocolStates.HeaderWait
		payload = list()
		payloadLength = 0
		while True:
			if not self.activeConnection:
				time.sleep(.1)
				continue
			try:
				rawQueue.append(self.serialPort.read(1))
			except serial.serialutil.SerialException as e:
				self.handleError(e)
				continue
			# print(rawQueue[-1], int.from_bytes(rawQueue[-1], byteorder='big'))
			if len(rawQueue) >= RAWQUEUESIZE:
				rawQueue.pop(0)

			# at this point we run the small state machine to accept messages
			if currentState == ProtocolStates.HeaderWait:
				if rawQueue[-1] == HEADER:
					currentState = ProtocolStates.LenGrab
			elif currentState == ProtocolStates.LenGrab:
				payloadLength = int.from_bytes(rawQueue[-1], byteorder='big')
				currentState = ProtocolStates.RecordingPayload
			elif currentState == ProtocolStates.RecordingPayload:
				payload.append(rawQueue[-1])
				if len(payload) >= payloadLength:
					currentState = ProtocolStates.TailCheck
			elif currentState == ProtocolStates.TailCheck:
				if rawQueue[-1] != TAIL:
					payload.insert(0, bytes([payloadLength]))
					payload.append(rawQueue[-1])
					self.handlePacketErrors('Tail not in right spot', payload)
					payload.clear()
					# print('Wrong Payload Length')

					currentState = ProtocolStates.HeaderWait
				else:
					currentState = ProtocolStates.ParseMessage
			elif currentState == ProtocolStates.ParseMessage:
				givenChecksum = int.from_bytes(rawQueue[-1], byteorder='big')
				newChecksum = self.calcChecksum(payload)
				if newChecksum == givenChecksum:
					# we now dispatch it to the appropriate handlers
					ID = int.from_bytes(payload[0], byteorder='big')
					if ID in self.callBackDict:
						for fp in self.callBackDict[ID]:
							# print('hi')
							fpThread = threading.Thread(target=functools.partial(fp, b''.join(payload)))
							fpThread.daemon = True
							fpThread.start()
							# fp(b''.join(payload))
					self.packetCountReceiving += 1
				else:
					payload.insert(0, bytes([payloadLength]))
					payload.append(rawQueue[-1])
					self.handlePacketErrors("Checksums did not Match 0X{:X} != 0X{:X}".format(newChecksum, givenChecksum), payload)
				payload.clear()
				currentState = ProtocolStates.HeaderWait
				# break
		return

	def handleOutGoing(self):
		while True:
			if self.activeConnection:
				try:
					newByte = self.outputQueue.get()
					self.serialPort.write(newByte.to_bytes(1, byteorder='big'))
				except serial.serialutil.SerialException as e:
					self.handleError(e)
					pass
			else:
				time.sleep(.1)
		return

	def handleError(self, inException):
		self.activeConnection = False
		# print(inException)
		for fp in self.errorBackList:
			fpThread = threading.Thread(target=functools.partial(fp, (inException)))
			fpThread.daemon = True
			fpThread.start()
		return

	def handlePacketErrors(self, errorMsg, payload):
		# print(payload)

		payload = b''.join(payload)
		# print(payload.hex().upper())
		for fp in self.packetDecodeErrorsBack:
			fpThread = threading.Thread(target=fp, args=[errorMsg, payload])
			fpThread.daemon = True
			fpThread.start()
		return


	def calcChecksum(self, inData):
		"""calculates checksum used for protocol, expects a byte array"""
		checksum = 0
		for inByte in inData:
			if type(inData) is list:
				inByte = int.from_bytes(inByte, byteorder='big')
			checksum = (((checksum & 0xFF) >> 1) + ((checksum & 0x1) << 7) + inByte) & 0xff
		return checksum

	def sendRawBytes(self, message):
		for x in message:
			self.outputQueue.put(x, block=False)
		return

	def sendRawMessage(self, payload):
		"""this is the basic sendMessage, this takes in a bytes payload and dismisses to the port"""
		message = bytearray()
		message += HEADER
		message += len(payload).to_bytes(1, byteorder='big')
		message += payload

		message += TAIL
		checksum = self.calcChecksum(payload)
		message += checksum.to_bytes(1, byteorder='big')
		message += bytes("\r\n".encode('ascii'))

		# print(message)
		for handler in self.outMessageCallBacks:
			fpThread = threading.Thread(target=functools.partial(handler, message))
			fpThread.daemon = True
			fpThread.start()
		self.sendRawBytes(message)
		self.packetCountSending += 1
		return

	def sendMessage(self, messageID, payload=None):
		"""this is just a wrapper to sendraw but we don't need to convert the ID ourselves"""
		if type(messageID) is not MessageIDs:
			return False
		if payload is None:
			self.sendRawMessage(int.to_bytes(messageID.value, 1, byteorder='big'))
		else:
			self.sendRawMessage(int.to_bytes(messageID.value, 1, byteorder='big')+payload)

	def requestLEDState(self):
		self.sendRawMessage(b'\x83')
		return

if __name__ == "__main__":
	import time
	import random


	def HandleDebug(inBytes):
		print(inBytes[1:].decode('ascii'))
		# print(inBytes)
		return

	def RawPackets(inBytes):
		print(inBytes)
		return

	def PrintLEDState(inBytes):
		print("LEDS: {:0X}".format(inBytes[1]))

	def HandlePong(inBytes):
		rawNumber = inBytes[1:]
		translatedNumber = int.from_bytes(rawNumber, byteorder='little')
		print("Pong Response", inBytes[1:], translatedNumber)
		# time.sleep(.2)





	from serial.tools import list_ports
	# print(serial.tools.list_ports.comports())
	print('Entering test harness for Protocol')

	newProtocol = Protocol()
	print(newProtocol.registerMessageHandler(MessageIDs.ID_DEBUG, HandleDebug))
	newProtocol.registerMessageHandler(MessageIDs.ID_DEBUG, RawPackets)
	newProtocol.registerMessageHandler(MessageIDs.ID_LEDS_STATE, PrintLEDState)
	newProtocol.registerMessageHandler(MessageIDs.ID_PONG, HandlePong)

	# activePort = serial.Serial('COM4', 115200)
	# print(activePort.readline())
	# newProtocol.sendRawBytes(bytes('Hello World'.encode('ascii')))
	# newProtocol.sendMessage(bytes('\x01Hello World'.encode('ascii')))
	# print(bytes('\x01Hello World'.encode('ascii')))
	# time.sleep(3)
	# newProtocol.sendMessage(bytes('\x01World Hello342'.encode('ascii')))
	# newProtocol.sendMessage(b'\x83')
	for i in range(10):
		ledMessage = b'\x81'+random.randint(0, 255).to_bytes(1, byteorder='big')
		newProtocol.sendRawMessage(ledMessage)
		newProtocol.sendRawMessage(b'\x83')
		time.sleep(.3)

	for i in range(3):
		newNumber = random.randint(0, 0xFFFFFFFF)
		print("Sending ping of {} and should get back {}".format(newNumber, newNumber>>1))
		message = MessageIDs.ID_PING.value.to_bytes(1,byteorder='big')+newNumber.to_bytes(4, byteorder='little')
		print(message)
		newProtocol.sendRawMessage(message)
		time.sleep(1.5)
	time.sleep(3)
