# -*- encoding: utf-8 -*-

import socket
import sys
from threading import Timer
from time import sleep
from ScriptRun import *

HOST = '172.8.1.102'    # The remote host
PORT = 8086              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

def process_data(data):
    parse_data = data.split('&')
    method = parse_data[0][7:]
    param = parse_data[1][7:-1].split(',')
    print type(method), type(param)
    # print('Method:%s,Param:%s,\n' % (method, list(param)))

    if method == 'help':
        on_help(list(param))

def recv_timer(sock):
    start_pos = 0
    end_pos = 0
    recv_data = ''

    while True:
        data = sock.recv(1024)
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
            process_data(recv_data);

        sleep(1)

timer = Timer(1,recv_timer,[s])
timer.start()


while True:
    send_data = raw_input(">>> ")
    if send_data == 'quit':
        break;
    if send_data.find('(') and send_data.find(')'):
        print('Invalid input\n')
    else:
        s.sendall( send_data + '()--end--')

print('Close Socket. quit program.')
timer.cancel()
s.close()

sys.exit(0)