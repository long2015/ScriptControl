#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from PyQt4 import QtCore
from PyQt4.QtGui import *
from ScriptControl import *

class ScriptWindow(QWidget):
    """docstring for ScriptWindow"""
    def __init__(self):
        super(ScriptWindow, self).__init__()

        self.data = ''
        self.connctState = False
        self.scriptctrl = ScriptCtrol()
        self.scriptctrl.attach(self.ReveiveFunc)
        print('attach Func:',self.ReveiveFunc)

        # create widget
        # 
        # device info: ip port
        self.setWindowTitle('ScriptAutoTest')
        self.ipLine = QLineEdit('10.33.8.164')
        self.portLine = QLineEdit('8080')
        self.connectButton = QPushButton('Connect',self)
        self.topGrid = QGridLayout()
        self.topGrid.addWidget(self.ipLine,0,0)
        self.topGrid.addWidget(self.portLine,0,3)
        self.topGrid.addWidget(self.connectButton,0,4)
        self.topGrid.setColumnStretch(0,3)
        self.topGrid.setColumnStretch(3,1)
        self.topGrid.setColumnStretch(4,3)

        # control command
        self.recordButton = QPushButton('Record', self)
        self.loadButton = QPushButton('Load', self)
        self.recordButton.setEnabled(False)
        self.loadButton.setEnabled(False)
        self.quitButton = QPushButton('Quit', self)
        self.toolGrid = QGridLayout()
        self.toolGrid.addWidget(self.recordButton,0,0)
        self.toolGrid.addWidget(self.loadButton,0,1)
        self.toolGrid.addWidget(self.quitButton,0,2)

        # text show widget
        self.textEdit = QTextEdit()

        # bottom layout
        self.inputEdit = QLineEdit()
        self.sendButton = QPushButton('Send', self)
        self.bottomLayout = QGridLayout()
        self.bottomLayout.addWidget(self.inputEdit,0,0)
        self.bottomLayout.addWidget(self.sendButton,0,1)

        # widget layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.toolGrid)
        self.mainLayout.addLayout(self.topGrid)
        self.mainLayout.addWidget(self.textEdit)
        self.mainLayout.addLayout(self.bottomLayout)
        self.setLayout(self.mainLayout)
        self.resize(400,300)

        # sigal slot
        self.connect(self.recordButton, QtCore.SIGNAL('clicked()'), self.OnRecord)
        self.connect(self.loadButton, QtCore.SIGNAL('clicked()'), self.OnLoadFile)
        self.connect(self.quitButton, QtCore.SIGNAL('clicked()'), self.OnQuit)
        self.connect(self.connectButton, QtCore.SIGNAL('clicked()'), self.OnConnect)
        self.connect(self.sendButton, QtCore.SIGNAL('clicked()'), self.OnSend)

    def OnConnect(self):
        scriptctrl = self.scriptctrl

        if scriptctrl.get_connstate() == False:
            ip = self.ipLine.text()
            port = int(self.portLine.text())
            print('ip:%s,port:%d' % (ip,port))

            scriptctrl.connect_dvr(ip, port)
        else:
            print('disconnect scriptctrl')
            scriptctrl.disconnect()

        # 
        state = scriptctrl.get_connstate()
        if state == False:
            self.connectButton.setText('Connect')
        else:
            self.connectButton.setText('Disconnect')

        self.recordButton.setEnabled(state)
        self.loadButton.setEnabled(state)
        self.ipLine.setDisabled(state)
        self.portLine.setDisabled(state)

    def ReveiveFunc(self,data):
        print('ReveiveFunc:%s,' % data)
        self.data += data

        # self.textEdit.setText(self.data)

    def OnSend(self):
        data = str(self.inputEdit.text())
        print('Type:',type(data))
        self.scriptctrl.send(data)

    def OnRecord(self):
        self.textEdit.setText('OnRecord')
        button = self.recordButton
        if button.text() == 'Record':
            button.setText('Stop')
        else:
            button.setText('Record')

    def OnLoadFile(self):
        self.textEdit.setText('loadButton')
        button = self.loadButton
        print(os.getenv('HOME'))
        filename = QFileDialog.getOpenFileName(self, 'Open file', 'C:/')
        self.textEdit.setText('fileName:%s,\n' % filename)

    def OnQuit(self):
        reply = QMessageBox.question(self, 'Quit', "Are you sure to quit?",
            QMessageBox.Yes,QMessageBox.No)
        if reply == QMessageBox.Yes:
            print('quit ')
            sys.exit(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = ScriptWindow()
    mainWindow.show()

    sys.exit(app.exec_())
