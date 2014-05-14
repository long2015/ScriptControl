#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from PyQt4 import QtCore
from PyQt4.QtGui import *
from ScriptControl import *
from language import *
class ScriptWindow(QWidget):
    """docstring for ScriptWindow"""
    def __init__(self):
        super(ScriptWindow,self).__init__()

        self.data = ''
        self.connctState = False
        self.scriptctrl = ScriptCtrol()
        self.scriptctrl.attach(self.ReveiveFunc)
        print('attach Func:',self.ReveiveFunc)

        # create widget
        # 
        # create top button
        self.newButton = QPushButton(tr('newscript'),self)
        self.editButton = QPushButton(tr('editscript'),self)
        self.loadButton = QPushButton(tr('loadscript'), self)
        self.runButton = QPushButton(tr('runscript'),self)
        self.recordButton = QPushButton(tr('record'), self)
        self.snapButton = QPushButton(tr('snapscreen'), self)

        self.loginButton = QPushButton(tr('login'),self)
        self.aboutButton = QPushButton(tr('about'), self)
        self.quitButton = QPushButton(tr('quit'),self)

        self.topGrid = QGridLayout()
        self.topGrid.addWidget(self.newButton,0,0)
        self.topGrid.addWidget(self.editButton,0,1)
        self.topGrid.addWidget(self.loadButton,0,2)
        self.topGrid.addWidget(self.runButton,0,3)
        self.topGrid.addWidget(self.recordButton,0,4)
        self.topGrid.addWidget(self.snapButton,0,5)
        self.topGrid.addWidget(self.loginButton,0,6)
        self.topGrid.addWidget(self.aboutButton,0,7)
        self.topGrid.addWidget(self.quitButton,0,8,2,2)

        # text show widget
        self.cmdListWidget = QListWidget()
        self.cmdListWidget.addItem(u'LClick<左键单击>')
        self.groupBox = QGroupBox(tr('commandlists'))
        self.listLayout = QVBoxLayout()
        self.listLayout.addWidget(self.cmdListWidget)
        self.groupBox.setLayout(self.listLayout)
        #
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        c = QColor(0x666666)
        self.textEdit.setTextColor(c)
        #
        self.textGrid = QGridLayout()
        self.textGrid.addWidget(self.groupBox,0,0)
        self.textGrid.addWidget(self.textEdit,0,3)
        self.textGrid.setColumnStretch(0,3)
        self.textGrid.setColumnStretch(3,7)
        
        # widget layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.topGrid)
        self.mainLayout.addLayout(self.textGrid)
        self.setLayout(self.mainLayout)
        self.resize(600,450)

        # sigal slot
        self.connect(self.recordButton, QtCore.SIGNAL('clicked()'), self.OnRecord)
        self.connect(self.loadButton, QtCore.SIGNAL('clicked()'), self.OnLoadFile)
        self.connect(self.snapButton, QtCore.SIGNAL('clicked()'), self.OnSnap)
        self.connect(self.quitButton, QtCore.SIGNAL('clicked()'), self.OnQuit)
        self.connect(self.loginButton, QtCore.SIGNAL('clicked()'), self.OnConnect)
        # self.connect(self.sendButton, QtCore.SIGNAL('clicked()'), self.OnSend)
        # self.connect(self.clearButton, QtCore.SIGNAL('clicked()'), self.OnClear)
        QtCore.QObject.connect(self, QtCore.SIGNAL("updateText()"), self.OnUpdate)
        self.connect(self.cmdListWidget, QtCore.SIGNAL('itemDoubleClicked(QListWidgetItem*)'),self.OnCmdDClick)
       
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
        button = self.recordButton
        if button.text() == 'Record':
            self.StartRec()
            button.setText('Stop')
        else:
            self.StopRec()
            button.setText('Record')
    def StartRec(self):
        filename = QFileDialog.getSaveFileName(self, 'Save file', './recod.txt')
        print filename
        self.scriptctrl.set_recfilename(filename)
        self.scriptctrl.send('startRec')

    def StopRec(self):
        self.scriptctrl.send('stopRec')

    def OnLoadFile(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', './')
        if not os.path.isfile(filename):
            return
        if self.scriptctrl.send_from_file(filename):
            self.data += 'send file successed!\n'
        else:
            self.data += 'send file Failed.\n'
        self.OnUpdate()

    def OnSnap(self):
        print("Snap one picture")
        self.scriptctrl.send("Screen('')")
        self.data += "Screen('')\n"
        self.OnUpdate()

    def OnQuit(self):
        reply = QMessageBox.question(self, 'Quit', "Are you sure to quit?",
            QMessageBox.Yes,QMessageBox.No)
        if reply == QMessageBox.Yes:
            print('quit ')
            self.scriptctrl.disconnect()
            print('quit ok')
            os._exit(0)

    def OnCmdDClick(self, item):
        cmd = str(item.text().toUtf8())
        pos = cmd.find('<')
        self.data += (cmd[:pos] + '()\n')
        self.OnUpdate()

    # key event
    def keyReleaseEvent(self, keyEvent):
        if keyEvent.key() == 0x01000004:
            if self.inputEdit.hasFocus():
                self.OnSend()
            elif self.connectButton.hasFocus():
                self.OnConnect()
        elif keyEvent.key() == 0x01000000:
            app.exit(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = ScriptWindow()
    mainWindow.show()

    sys.exit(app.exec_())
