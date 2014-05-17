# -*- encoding: utf-8 -*-

from ScriptRun import *
import socket
import sys
import os
from threading import Timer
from time import sleep
import json

HOST = '192.168.1.56'    # The remote host
PORT = 8086             # The same port as used by the server

class ScriptCtrol(object):
    """docstring for ClassName"""
    def __init__(self):
        self.socket = None
        self.sigfunc = None
        self.connct_state = False
        self.receive_loop = True
        self.record_filename = None
        self.timer = None
        self.data_processer = DataProcesser()

    def attach(self,func):
        self.sigfunc = func

    def connect_dvr(self, ip, port):
        if self.get_connstate() == True:
            return True
        print('ip:%s,port:%d' % (ip,port))
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))

        self.connct_state = True
        #start timer to receive data
        self.receive_loop = True


        if self.connct_state:
            # 
            self.timer = Timer(1,self.recv_timer)
            self.timer.start()
            # sleep(1)
            self.send('getcommands()')

    def disconnect(self):
        if self.get_connstate() == False:
            return True

        self.receive_loop = False
        self.timer.cancel()
        del self.timer
        self.timer = None

        if self.socket != None:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
            self.socket = None
        self.connct_state = False

    def get_connstate(self):
        return self.connct_state

    def preprocess(self, data):
        l = data.split(' ')
        if l[0] == 'startRec':
            self.set_recfilename(l[1])
            return 'startRec'
        return data

    def set_recfilename(self, filename):
        self.data_processer.set_recfilename(filename)

    def process_data(self, data):
        # print('Data', data)
        #dictdata = eval(data)
        result = self.data_processer.process(data)
        # print('method:',dictdata['method'],result)
        if result != None and self.sigfunc != None:
            self.sigfunc(result)

        print result

    def send(self, data):
        # self.socket.sendall('--start--' + data + '--end--')
        self.socket.sendall(data + '--end--')

    def send_from_file(self, filepath):
        if os.path.isfile(filepath) == False:
            return False

        f = open(filepath,'r')
        while True:
            data = f.read(1024)
            if not data:
                break
            self.socket.sendall(data)
        self.socket.sendall('--end--')
        return True

    def recv_timer(self):
        start_pos = 0
        end_pos = 0
        recv_data = ''
        total = 0
        while self.receive_loop:
            data = ''
            data = self.socket.recv(64*1024)

            print('type',type(data),len(data))
            # print('ReceiveData[%s]\n' % repr(data))
            total += len(data)
            print "len: ",total
            start_pos = data.find('--start--')
            end_pos = data.find('--end--')
            # print start_pos,end_pos

            if start_pos != -1 and end_pos == -1:
                recv_data = data[start_pos:]
            elif start_pos == -1 and end_pos == -1:
                recv_data += data
            elif end_pos != -1:
                if start_pos != -1:
                    recv_data = data[start_pos:end_pos+7]
                else:
                    recv_data += data[:end_pos+7]

                # parse data and do it
                if recv_data.find('--start--') != -1 and recv_data.find('--end--') != -1:
                    self.process_data(recv_data[9:-7]);
                else:
                    print 'error data'
                # process finish clear data
                recv_data = ''

            # sleep(1)
        print('Exit recv_timer()')

if __name__ == '__main__':
    script_client = ScriptCtrol()
    script_client.connect_dvr(HOST,PORT)

    while True:
        send_data = raw_input(">>> ")
        if len(send_data) == 0:
            continue
        elif send_data == 'quit':
            break
        else:
            send_data = script_client.preprocess(send_data)

        script_client.send(send_data)

    print('Close Socket. quit program.')
    script_client.disconnect()
    os._exit(0)