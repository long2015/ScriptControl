#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from PyQt4 import QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ScriptControl import *
from language import *
class LoginDialog(QDialog):
    """docstring for LoginDialog"""
    def __init__(self):
        super(LoginDialog, self).__init__()

        self.ipLine = QLineEdit('172.8.1.101')
        self.portLine = QLineEdit('8086')
        self.label = QLabel()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.ipLine)
        self.layout.addWidget(self.portLine)
        self.layout.addWidget(self.label)
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)

        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)
        self.setWindowTitle('Login Device')
 
        self.connect(self.buttons, QtCore.SIGNAL('accepted()'),self.OnOK)
        self.connect(self.buttons, QtCore.SIGNAL('rejected()'),self.OnCanle)

    def check(self):
        if self.ipLine.text() == '' or self.portLine.text() == '':
            self.label.setText('IP or Port is null')
            return False
        else:
            return True

    def OnOK(self):
        if self.check():
            QDialog.done(self,QDialog.Accepted)
    def OnCanle(self):
        QDialog.done(self,QDialog.Rejected)

    def Data(self):
        return self.ipLine.text(),self.portLine.text()

    @staticmethod
    def GetIpPort():
        dialog = LoginDialog()
        result = ( dialog.exec_() == QDialog.Accepted )

        ip,port = '',0
        if result:
            ip,port = dialog.Data()
            print ip,port
            return str(ip), int(port), result
        else:
            return ip, port, result

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
        self.openButton = QPushButton(tr('openscript'), self)
        self.editButton = QPushButton(tr('editscript'),self)
        self.runButton = QPushButton(tr('runscript'),self)
        self.recordButton = QPushButton(tr('record'), self)
        self.snapButton = QPushButton(tr('snapscreen'), self)
        # self.lable = QLabel('',self)
        self.loginButton = QPushButton(tr('login'),self)
        self.aboutButton = QPushButton(tr('about'), self)
        self.quitButton = QPushButton(tr('quit'),self)

        self.topGrid = QHBoxLayout()
        self.topGrid.addWidget(self.newButton)
        self.topGrid.addWidget(self.openButton)
        self.topGrid.addWidget(self.editButton)
        self.topGrid.addWidget(self.runButton)
        self.topGrid.addWidget(self.recordButton)
        self.topGrid.addWidget(self.snapButton)
        self.topGrid.addWidget(self.loginButton)
        self.topGrid.addWidget(self.aboutButton)
        self.topGrid.addWidget(self.quitButton)
        # self.topGrid.addWidget(self.lable)
        # self.topGrid.setStretchFactor (self.lable,1)
        # adjust the widget
        for i in range(self.topGrid.count()):
            item = self.topGrid.itemAt(i)
            item.widget().setMinimumWidth(60)
            item.widget().setMinimumHeight(40)


        # text show widget
        self.cmdListWidget = QListWidget()
        self.groupBox = QGroupBox(tr('commandlists'))
        self.listLayout = QVBoxLayout()
        self.listLayout.addWidget(self.cmdListWidget)
        self.groupBox.setLayout(self.listLayout)

        #

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        palette = QPalette()
        palette.setColor(QPalette.Text, Qt.black)
        palette.setColor(QPalette.Base, Qt.lightGray)
        self.textEdit.setPalette(palette)
        font = QFont("Courier")
        self.textEdit.setCurrentFont(font)
        metrics = QFontMetrics(font);
        self.textEdit.setTabStopWidth(4*metrics.width(' '))

        #
        self.textGrid = QGridLayout()
        self.textGrid.addWidget(self.groupBox,0,0)
        self.textGrid.addWidget(self.textEdit,0,2)
        self.textGrid.setColumnStretch(2,8)
        
        # widget layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.topGrid)
        self.mainLayout.addLayout(self.textGrid)
        self.setLayout(self.mainLayout)
        self.setWindowTitle('Dahua Demon v0.1')
        self.setMinimumSize(740,620)
        self.setMaximumSize(740,620)

        # sigal slot
        self.connect(self.newButton, QtCore.SIGNAL('clicked()'), self.OnNewFile)
        self.connect(self.recordButton, QtCore.SIGNAL('clicked()'), self.OnRecord)
        self.connect(self.openButton, QtCore.SIGNAL('clicked()'), self.OnOpenFile)
        self.connect(self.runButton, QtCore.SIGNAL('clicked()'), self.OnRunScript)
        self.connect(self.snapButton, QtCore.SIGNAL('clicked()'), self.OnSnap)
        self.connect(self.quitButton, QtCore.SIGNAL('clicked()'), self.OnQuit)
        self.connect(self.loginButton, QtCore.SIGNAL('clicked()'), self.OnConnect)
        # self.connect(self.clearButton, QtCore.SIGNAL('clicked()'), self.OnClear)
        self.connect(self.aboutButton, QtCore.SIGNAL('clicked()'), self.OnAbout)
        QtCore.QObject.connect(self, QtCore.SIGNAL("updateText()"), self.OnUpdate)
        QtCore.QObject.connect(self, QtCore.SIGNAL('updatelist()'), self.OnUpdateList)
        self.connect(self.cmdListWidget, QtCore.SIGNAL('itemDoubleClicked(QListWidgetItem*)'),self.OnCmdDClick)

    def OnConnect(self):
        scriptctrl = self.scriptctrl

        if scriptctrl.get_connstate() == False:
            ip,port,result = LoginDialog.GetIpPort()
            print ip,port,result
            if result == False:
                return

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
            self.setWindowTitle('%s:%d - Dahua Demon' % (ip,port))

        self.recordButton.setEnabled(state)
        self.openButton.setEnabled(state)
        # self.ipLine.setDisabled(state)
        # self.portLine.setDisabled(state)

    def OnUpdate(self):
        print('OnUpdate')
        self.textEdit.setPlainText(self.data)

    def OnUpdateList(self):
        for i in self.cmdlist:
            print i
            self.cmdListWidget.addItem(i+' <>')

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

    def OnNewFile(self):
        self.textEdit.setReadOnly(False)
        self.textEdit.setFocus()
        self.data = ''
        self.OnUpdate()

    def OnOpenFile(self):
        # tips 
        # save current file

        # chose a file to open
        filename = QFileDialog.getOpenFileName(self, 'Open file', './')
        if not os.path.isfile(filename):
            return

        f = open(filename)
        self.data = ''
        for line in f.readlines():
            self.data += line.decode('utf-8')
        self.textEdit.setReadOnly(False)

        self.OnUpdate()

    def OnRunScript(self):
        data = str(self.textEdit.toPlainText())
        print type(data),data
        self.scriptctrl.send(data)

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
        print cmd
        pos = cmd.find(' <')
        self.data += (cmd[:pos] + '()\n')
        self.OnUpdate()

    def OnAbout(self):
        QMessageBox.information(self,QtCore.QString('About'),
                QtCore.QString('Dehua Demon v0.1\nto DahuaYanFa'))

    # key event
    def keyReleaseEvent(self, keyEvent):
        if keyEvent.key() == 0x01000004:
            if self.connectButton.hasFocus():
                self.OnConnect()
        elif keyEvent.key() == 0x01000000:
            app.exit(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash=QSplashScreen(QPixmap("pic/newscript.png"))
    splash.show()
    mainWindow = ScriptWindow()
    mainWindow.show()
    splash.finish(mainWindow)
    sys.exit(app.exec_())
