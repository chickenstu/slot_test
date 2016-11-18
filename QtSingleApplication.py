"""
    The MIT License
    Copyright 2011 Thomas Dall'Agnese <thomas.dallagnese@gmail.com>
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
"""
"""
    Modifications by Vladimir Nachbaur:
    Send receiveArgs signal when args are received instead of calling a
    method from mainWindow and connects to mainWindow receiveArgs slot
"""

from PySide import QtCore
from PySide.QtGui import QMessageBox, QApplication
from PySide.QtCore import QIODevice, QTimer, QCoreApplication
from PySide.QtNetwork import QLocalServer, QLocalSocket
import sys

class QSingleApplication(QApplication):
    # Signal sent when another instance is launched with arguments
    argsReceived = QtCore.Signal((str,))

    # Start the application,
    # either as a server (first instance) or as a client
    # others clients only send the argv they have been given and exit
    def singleStart(self, mainWindow):
        print "singleStart() function from QSingleApp got called."
        self.mainWindow = mainWindow
        # Socket
        self.m_socket = QLocalSocket()
        # Connected, error are signals that are being emitted
        self.m_socket.connected.connect(self.connectToExistingApp)
        self.m_socket.error.connect(self.startApplication)
        self.m_socket.connectToServer(self.applicationName(), QIODevice.WriteOnly)

    # used for the very first instance to create the main window and start server
    def startApplication(self):
        self.m_server = QLocalServer()
        print "startApplication() function from QSingleApplication got called"
        # Returns bool (True on success). Tells server to listen for incoming connections on 'name'
        if self.m_server.listen(self.applicationName()):
            print "Server is listening .... startApplication() function from QSingleApp"
            self.m_server.newConnection.connect(self.getNewConnection)
            # After emitting a signal, connecting it to the UI class function
            self.argsReceived.connect(self.mainWindow.receive_args)
            self.mainWindow.show()
        else:
            QMessageBox.critical(None, self.tr("Error"), self.tr("Error listening the socket."))

    # used by later instances to send argv to the main instance
    def connectToExistingApp(self):
        if len(sys.argv) > 1 and sys.argv[1] is not None:
            self.m_socket.write(sys.argv[1])
            print "exiting new app A"
            self.m_socket.bytesWritten.connect(self.quit)
        else:
            print "exiting new app B"
            self.m_socket.write("--show")
            self.m_socket.bytesWritten.connect(self.quit)

    def getNewConnection(self):
        print "getNewConnection() was called"
        self.mainWindow.show()
        self.new_socket = self.m_server.nextPendingConnection()
        self.new_socket.readyRead.connect(self.readSocket)

    def readSocket(self):
        print "readSocket() function in QSingleApplication.py"
        f = self.new_socket.readLine()
        self.argsReceived.emit(str(f))
