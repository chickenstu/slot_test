from PySide.QtGui import QMainWindow, QApplication, QWidget, QPushButton
from PySide.QtCore import *
import sys


class mainChild(QWidget):
	def __init__(self, parent=None):
		super(mainChild, self).__init__(parent)
		self.setWindowTitle("child window that's right")
		self.setGeometry(00, 100, 400, 400)
		self.button = QPushButton("I Should appear in separate Window!!", self)
		self.show()


class mainWin(QMainWindow):
	def __init__(self):
		super(mainWin, self).__init__()
		self.setWindowTitle("main window that's right")
		self.setGeometry(100, 100, 300, 300)
		self.myChild = None
		self.statusBar().showMessage("test")
		self.button = QPushButton("child dialog", self)
		self.button.clicked.connect(self.openChild)
		self.show()

	def openChild(self):
		self.myChild = mainChild(self)


if __name__ == "__main__":
	print "aight"
	app = QApplication(sys.argv)
	print "yes"
	test = mainWin()
	sys.exit(app.exec_())
