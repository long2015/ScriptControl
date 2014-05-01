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
        self.ipLine = QLineEdit('192.168.1.56')
        self.portLine = QLineEdit('8080')
        self.connectButton = QPushButton('Connect',self)
        self.connectButton.setFocus()
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
        self.textEdit.setReadOnly(True)
        c = QColor(0x666666)
        self.textEdit.setTextColor(c)

        # bottom layout
        self.inputEdit = QLineEdit()
        self.sendButton = QPushButton('Send', self)
        self.clearButton = QPushButton('clear', self)
        self.bottomLayout = QGridLayout()
        self.bottomLayout.addWidget(self.inputEdit,0,0)
        self.bottomLayout.addWidget(self.sendButton,0,1)
        self.bottomLayout.addWidget(self.clearButton,0,2)

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
        self.connect(self.clearButton, QtCore.SIGNAL('clicked()'), self.OnClear)
        QtCore.QObject.connect(self, QtCore.SIGNAL("updateText()"), self.OnUpdate)

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
            self.inputEdit.setFocus()

        self.recordButton.setEnabled(state)
        self.loadButton.setEnabled(state)
        self.ipLine.setDisabled(state)
        self.portLine.setDisabled(state)

    def OnUpdate(self):
        print('OnUpdate')
        self.textEdit.setText(self.data)

    def ReveiveFunc(self,data):
        print('ReveiveFunc:%s,' % data)
        self.data += (data + '\n')
        self.emit(QtCore.SIGNAL("updateText()"))

    def OnSend(self):
        data = str(self.inputEdit.text())
        if len(data) == 0:
            return

        print('Type:',type(data))
        self.data += (data + '\n')
        self.OnUpdate()
        self.inputEdit.setText('')
        self.scriptctrl.send(data)

    def OnClear(self):
        self.data = ''
        self.OnUpdate()

    def OnRecord(self):
        self.textEdit.setText('OnRecord')
        button = self.recordButton
        if button.text() == 'Record':
            button.setText('Stop')
        else:
            button.setText('Record')

    def OnLoadFile(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', './')
        if self.scriptctrl.send_from_file(filename):
            self.data += 'send file successed!\n'
        else:
            self.data += 'send file Failed.\n'
        self.OnUpdate()

    def OnQuit(self):
        reply = QMessageBox.question(self, 'Quit', "Are you sure to quit?",
            QMessageBox.Yes,QMessageBox.No)
        if reply == QMessageBox.Yes:
            print('quit ')
            app.exit(0)

    # key event
    def keyReleaseEvent(self, keyEvent):
        if keyEvent.key() == 0x01000004 and self.inputEdit.hasFocus():
            self.OnSend()
        elif keyEvent.key() == 0x01000000:
            app.exit(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = ScriptWindow()
    mainWindow.show()

    sys.exit(app.exec_())
