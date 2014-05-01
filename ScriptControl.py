# -*- encoding: utf-8 -*-

from ScriptRun import *
import socket
import sys
import os
from threading import Timer
from time import sleep
import json

HOST = '172.8.1.101'    # The remote host
PORT = 8086             # The same port as used by the server

methodlist = {}
methodlist['help'] = on_help
methodlist['startRec'] = on_startRec
# methodlist['sopRec'] = on_stopRec

class ScriptCtrol(object):
    """docstring for ClassName"""
    def __init__(self):
        self.socket = None
        self.sigfunc = None
        self.connct_state = False
        self.receive_loop = True
        self.record_file = None

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

    def preprocess(self, data):
        data = data.split(' ')
        if data[0] == 'startRec':
            self.pre_startRec(data[1])

        return 'startRec'

    def pre_startRec(self, file):
        self.record_file = open(file,'w')

    def process_data(self, data):
        print('Data', data)
        data_dict = eval(data)
        # print('Dict', data_dict)
        method = data_dict['method']
        if method == 'stopRec':
            print 'close file '
            self.record_file.close()
            self.record_file = None
            return

        func = methodlist[method]
        print '\n\nMeths type:',type(func)
        if func != None:
            result = func(data_dict['param'])
            if method == 'startRec':
                print type(result)
                self.record_file.write(result)

            if self.sigfunc != None:
                self.sigfunc(result)
            print result
        else:
            print('No Support Command:%s' % method)

    def send(self, data):
        if data.find('(') == -1 and data.find(')') == -1:
            data += '()'

        self.socket.sendall('--start--' + data + '--end--')
    def send_from_file(self, filepath):
        if os.path.isfile(filepath) == False:
            return False

        f = open(filepath,'r')
        while True:
            data = f.read(1024)
            if not data:
                break

            self.send(data)

        return True

    def recv_timer(self):
        start_pos = 0
        end_pos = 0
        recv_data = ''

        while self.receive_loop:
            data = self.socket.recv(1024)
            print('ReceiveData[%s]\n' % repr(data))
            start_pos = data.find('--start--')
            end_pos = data.find('--end--')
            # print start_pos,end_pos

            if start_pos != -1 and end_pos == -1:
                start_pos += 10
                recv_data = data[start_pos+9:]
            elif start_pos == -1 and end_pos == -1:
                recv_data += data
            elif end_pos != -1:
                if start_pos != -1:
                    recv_data = data[start_pos+9:end_pos]
                else:
                    recv_data += data[:end_pos]

                # parse data and do it
                self.process_data(recv_data);
                # process finish clear data
                recv_data = ''

            sleep(1)
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
            send_data = self.preprocess(send_data)

        script_client.send(send_data)

    print('Close Socket. quit program.')
    script_client.disconnect()

    sys.exit(0)