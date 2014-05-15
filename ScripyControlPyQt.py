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
        self.cmdlist = []
        self.connctState = False
        self.scriptctrl = ScriptCtrol()
        self.scriptctrl.attach(self.ReveiveFunc)
        print('attach Func:',self.ReveiveFunc)

        # icon
        new_icon = QIcon('new.pngd')

        # create widget
        # 
        # create top button
        # how to change the button size???
        self.newButton = QPushButton(tr('newscript'),self)
        self.newButton.setIcon(new_icon)
        self.newButton.setIconSize(QtCore.QSize(10,30))

        self.editButton = QPushButton(tr('editscript'),self)
        self.loadButton = QPushButton(tr('loadscript'), self)
        self.runButton = QPushButton(tr('runscript'),self)
        self.recordButton = QPushButton(tr('record'), self)
        self.snapButton = QPushButton(tr('snapscreen'), self)
        self.lable = QLabel('',self)
        self.loginButton = QPushButton(tr('login'),self)
        self.aboutButton = QPushButton(tr('about'), self)
        self.quitButton = QPushButton(tr('quit'),self)

        self.topGrid = QHBoxLayout()
        self.topGrid.addWidget(self.newButton)
        self.topGrid.addWidget(self.editButton)
        self.topGrid.addWidget(self.loadButton)
        self.topGrid.addWidget(self.runButton)
        self.topGrid.addWidget(self.recordButton)
        self.topGrid.addWidget(self.snapButton)
        self.topGrid.addWidget(self.loginButton)
        self.topGrid.addWidget(self.aboutButton)
        self.topGrid.addWidget(self.quitButton)
        self.topGrid.addWidget(self.lable)
        self.topGrid.setStretchFactor (self.lable,1)

        # text show widget
        self.cmdListWidget = QListWidget()
        # self.cmdListWidget.addItem(u'LClick<左键单击>')
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
        self.textGrid.setColumnStretch(3,7)
        
        # widget layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.topGrid)
        self.mainLayout.addLayout(self.textGrid)
        self.setLayout(self.mainLayout)
        self.resize(740,620)
        # sigal slot
        self.connect(self.recordButton, QtCore.SIGNAL('clicked()'), self.OnRecord)
        self.connect(self.loadButton, QtCore.SIGNAL('clicked()'), self.OnLoadFile)
        self.connect(self.snapButton, QtCore.SIGNAL('clicked()'), self.OnSnap)
        self.connect(self.quitButton, QtCore.SIGNAL('clicked()'), self.OnQuit)
        self.connect(self.loginButton, QtCore.SIGNAL('clicked()'), self.OnConnect)
        # self.connect(self.sendButton, QtCore.SIGNAL('clicked()'), self.OnSend)
        # self.connect(self.clearButton, QtCore.SIGNAL('clicked()'), self.OnClear)
        QtCore.QObject.connect(self, QtCore.SIGNAL("updateText()"), self.OnUpdate)
        QtCore.QObject.connect(self, QtCore.SIGNAL('updatelist()'), self.OnUpdateList)
        self.connect(self.cmdListWidget, QtCore.SIGNAL('itemDoubleClicked(QListWidgetItem*)'),self.OnCmdDClick)

    def OnConnect(self):
        scriptctrl = self.scriptctrl

        if scriptctrl.get_connstate() == False:
            ip = '172.8.1.101'
            port = 8086
            print('ip:%s,port:%d' % (ip,port))

            scriptctrl.connect_dvr(ip, port)
        else:
            print('disconnect scriptctrl')
            scriptctrl.disconnect()
            self.cmdListWidget.clear()

        # 
        state = scriptctrl.get_connstate()
        if state == False:
            self.loginButton.setText(tr('login'))
        else:
            self.loginButton.setText(tr('logout'))

        self.recordButton.setEnabled(state)
        self.loadButton.setEnabled(state)
        # self.ipLine.setDisabled(state)
        # self.portLine.setDisabled(state)

    def OnUpdate(self):
        print('OnUpdate')
        self.textEdit.setText(self.data)

    def OnUpdateList(self):
        for i in self.cmdlist:
            print i
            self.cmdListWidget.addItem(i)

    def ReveiveFunc(self,data):
        print('ReveiveFunc:%s,' % data[0])
        if data[0] == 'getcommands':
            self.cmdlist = data[1]
            self.emit(QtCore.SIGNAL('updatelist()'))
        else:
            self.data += (data[1] + '\n')
            self.emit(QtCore.SIGNAL("updateText()"))

    def OnSend(self):
        if len(data) == 0:
            return

        print('Type:',type(data))
        self.data += (data + '\n')
        self.OnUpdate()
        self.scriptctrl.send(data)

    def OnClear(self):
        self.data = ''
        self.OnUpdate()

    def OnRecord(self):
        button = self.recordButton
        if button.text() == tr('record'):
            self.StartRec()
            button.setText(tr('stop'))
        else:
            self.StopRec()
            button.setText(tr('record'))

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
            if self.connectButton.hasFocus():
                self.OnConnect()
        elif keyEvent.key() == 0x01000000:
            app.exit(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = ScriptWindow()
    mainWindow.show()

    sys.exit(app.exec_())
