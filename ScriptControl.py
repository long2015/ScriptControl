# -*- encoding: utf-8 -*-

import socket
import sys
from threading import Timer
from time import sleep
from ScriptRun import *

HOST = '172.8.1.101'    # The remote host
PORT = 8086             # The same port as used by the server

Methods = {}
Methods['help'] = on_help

class ScriptCtrol(object):
    """docstring for ClassName"""
    def __init__(self):
        self.socket = None
        self.sigfunc = None
        self.connct_state = False
        self.receive_loop = True

    def attach(self,func):
        self.sigfunc = func

    def connect_dvr(self, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))

        self.connct_state = True
        #start timer to receive data
        self.timer = Timer(1,self.recv_timer)
        self.receive_loop = True
        self.timer.start()

    def disconnect(self):
        self.receive_loop = False
        self.timer.cancel()
        self.socket.close()
        self.connct_state = False

    def get_connstate(self):
        return self.connct_state

    def process_data(self, data):
        # parse_data = data.split('&')
        # method = parse_data[0][7:]
        # param = parse_data[1][7:-1].split(',')
        # print type(method), type(param)
        # print('Method:%s,Param:%s,\n' % (method, list(param)))
        print('Data', data)
        if self.sigfunc != None:
                self.sigfunc(data)
        return
        
        func = Methods[method]
        print '\n\nMeths type:',type(func)
        if func != None:
            result = func(list(param))
            print('Func:', self.sigfunc)
            if self.sigfunc != None:
                self.sigfunc(result)
            print result
        else:
            print('No Support Command:%s' % method)

    def send(self, data):
        if data.find('(') == -1 and data.find(')') == -1:
            data += '()'

        self.socket.sendall(data + '--end--')

    def recv_timer(self):
        start_pos = 0
        end_pos = 0
        recv_data = ''

        while self.receive_loop:
            data = self.socket.recv(1024)
            print('ReceiveData[%s]\n' % repr(data))
            start_pos = data.find('--start--\n')
            end_pos = data.find('--end--')
            # print start_pos,end_pos

            if start_pos != -1 and end_pos == -1:
                start_pos += 10
                recv_data = data[start_pos:]
            elif start_pos == -1 and end_pos != -1:
                recv_data += data[:end_pos]
                # parse data and do it
                self.process_data(recv_data);

            sleep(1)
        print('Exit recv_timer()')

if __name__ == '__main__':
    script_client = ScriptCtrol()
    script_client.connect_dvr(HOST,PORT)

    while True:
        send_data = raw_input(">>> ")
        if send_data == 'quit':
            break
        elif len(send_data) == 0:
            continue

        script_client.send(send_data)

    print('Close Socket. quit program.')
    script_client.disconnect()

    sys.exit(0)