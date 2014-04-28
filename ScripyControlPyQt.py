#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtGui import *

class ScriptWindow(QWidget):
    """docstring for ScriptWindow"""
    def __init__(self):
        super(ScriptWindow, self).__init__()

        self.connctState = False

        # create widget

        # device info: ip port
        self.setWindowTitle('ScriptAutoTest')
        self.ipLine = QLineEdit()
        self.portLine = QLineEdit()
        self.connectButton = QPushButton('Connect',self)
        self.topGrid = QGridLayout()
        self.topGrid.addWidget(self.ipLine,0,0)
        self.topGrid.addWidget(self.portLine,0,6)
        self.topGrid.addWidget(self.connectButton,0,7)
        self.topGrid.setColumnStretch(0,6)
        self.topGrid.setColumnStretch(6,1)
        self.topGrid.setColumnStretch(7,3)

        # control command
        self.recordButton = QPushButton('Record', self)
        self.loadButton = QPushButton('Load', self)
        self.quitButton = QPushButton('Quit', self)
        self.toolGrid = QGridLayout()
        self.toolGrid.addWidget(self.recordButton,0,0)
        self.toolGrid.addWidget(self.loadButton,0,1)
        self.toolGrid.addWidget(self.quitButton,0,2)

        # text show widget
        self.textEdit = QTextEdit()

        # widget layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.topGrid)
        self.mainLayout.addLayout(self.toolGrid)
        self.mainLayout.addWidget(self.textEdit)
        self.setLayout(self.mainLayout)
        self.resize(400,300)

        # sigal slot
        self.connect(self.recordButton, QtCore.SIGNAL('clicked()'), self.OnRecord)
        self.connect(self.loadButton, QtCore.SIGNAL('clicked()'), self.OnLoadFile)
        self.connect(self.quitButton, QtCore.SIGNAL('clicked()'), self.OnQuit)
        self.connect(self.connectButton, QtCore.SIGNAL('clicked()'), self.OnConnect)

    def OnConnect(self):
        if self.connctState:
            self.ipLine.setDisabled(True)
            self.portLine.setDisabled(True)
            self.connectButton.setText('Disconnect')
            self.connctState = False
        else:
            self.ipLine.setEnabled(True)
            self.portLine.setEnabled(True)
            self.connectButton.setText('Connect')
            self.connctState = True

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
        reply = QtGui.QMessageBox.question(self, 'Quit', "Are you sure to quit?",
            QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            print('quit ')
            sys.exit(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = ScriptWindow()
    mainWindow.show()

    sys.exit(app.exec_())
