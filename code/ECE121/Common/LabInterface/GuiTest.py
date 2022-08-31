import sys
import random
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import PyQt5




if hasattr(PyQt5.QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(PyQt5.QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(PyQt5.QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(PyQt5.QtCore.Qt.AA_UseHighDpiPixmaps, True)


class bar(QWidget):
	def __init__(self, numLabels, parent=None):
		super(bar, self).__init__(parent)
		self.layoutUsed = QVBoxLayout()
		self.setLayout(self.layoutUsed)
		self.layoutUsed.addWidget(QLabel("Hi Bob"))
		for i in range(numLabels):
			newLabel = QLabel("Wee: {}/{}".format(i, numLabels))
			self.layoutUsed.addWidget(newLabel)
		# self.show()
		return

class Foo(QDialog):
	def __init__(self, parent=None):
		super(Foo, self).__init__(parent)
		self.outerLayout = QVBoxLayout()


		self.setLayout(self.outerLayout)


		self.setWindowTitle('Dummy Gui')

		self.tabs = QTabWidget()
		self.outerLayout.addWidget(self.tabs)

		self.tabs.addTab(bar(5), "hi")
		self.tabs.addTab(bar(1), "Bob")


		# self.testBar = bar(5)
		# self.outerLayout.addWidget(self.testBar)
		# self.testBar = bar(5)
		# self.outerLayout.addWidget(self.testBar)


		self.outerLayout.addWidget(QLabel("Series Local Name"))
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