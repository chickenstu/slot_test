import sys
from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtNetwork import *
from QtSingleApplication import QSingleApplication


class testClass(QWidget):
	"""
	Main class of the Directory Manager Application
	"""
	def __init__(self):
		super(testClass, self).__init__()
		self.setWindowTitle("test bro")
		self.resize(300, 300)

	@Slot(str)
	def receive_args(self, args):
		print "hello"
		self.raise_()


if __name__ == '__main__':
	app = QSingleApplication(sys.argv)
	app.setApplicationName("ManuTest")
	#print "App name test:", app.applicationName()
	myWindow = testClass()
	app.singleStart(myWindow)
	sys.exit(app.exec_())
