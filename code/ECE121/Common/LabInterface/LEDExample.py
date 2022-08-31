from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5
import sys
import random
from ece121 import Protocol




if hasattr(PyQt5.QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(PyQt5.QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(PyQt5.QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(PyQt5.QtCore.Qt.AA_UseHighDpiPixmaps, True)



class Foo(QDialog):
	def __init__(self, parent=None):
		super(Foo, self).__init__(parent)
		self.outerLayout = QVBoxLayout()
		self.setLayout(self.outerLayout)
		self.setWindowTitle('Dummy Gui')

		self.outerLayout.addWidget(QLabel("LED Setting Example"))
		checkLayout = QHBoxLayout()

		self.outerLayout.addLayout(checkLayout)

		self.ledCheckButtons = list()
		for i in range(7, -1, -1):
			newCheck = QCheckBox("{}".format(i))
			# newCheck.setTristate(False)
			checkLayout.addWidget(newCheck)
			newCheck.clicked.connect(self.handleLEDOut)
			self.ledCheckButtons.append(newCheck)

		# self.setCheckBoxes(random.randint(0, 255))
		print(self.getCheckBoxes())

		# we now instantiate a copy of the protocol and link it to the led message
		self.protInstance = Protocol.Protocol()
		self.protInstance.registerMessageHandler(Protocol.MessageIDs.ID_LEDS_STATE, self.handleLEDIn)
		self.protInstance.registerMessageHandler(Protocol.MessageIDs.ID_DEBUG, self.updateDebug)

		# send a request for current LED state

		self.protInstance.requestLEDState()

		# add a label for debug messages

		self.debugLabel = QLabel()

		self.outerLayout.addWidget(self.debugLabel)

		return

	def setCheckBoxes(self, inPattern):
		print(inPattern)
		for index, check in enumerate(self.ledCheckButtons):
			# print(check)
			# print(index)
			if inPattern & (1 << (7-index)):
				check.setCheckState(2)
			else:
				check.setCheckState(0)

	def getCheckBoxes(self):
		outPattern = 0
		for index, check in enumerate(self.ledCheckButtons):
			if check.checkState() == 2:
				outPattern |= (1 << (7-index))
		return outPattern

	def handleLEDIn(self, inBytes):
		self.setCheckBoxes(inBytes[1])
		return

	def handleLEDOut(self):
		ledPattern = self.getCheckBoxes()
		print(ledPattern)
		messageOut = Protocol.MessageIDs.ID_LEDS_SET.value.to_bytes(1, byteorder='big')
		messageOut += ledPattern.to_bytes(1, byteorder='big')
		# print(messageOut)
		self.protInstance.sendRawMessage(messageOut)
		return

	def updateDebug(self, inBytes):
		self.debugLabel.setText(inBytes[1:].decode('ascii'))
		return

sys._excepthook = sys.excepthook

def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(0)

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook

app = QApplication(sys.argv)
gui = Foo()
gui.show()
app.exec_()