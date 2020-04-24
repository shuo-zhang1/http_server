# Shuo Zhang
# 21801147
# Section 102
#! /usr/bin/env python3
# HTTP Client

import sys
import socket
import struct
import random
import datetime, time
import os.path

url = sys.argv[1]
url = url.split('/')
host = url[0].split(':')[0]
port = url[0].split(':')[1]
filename = url[1]
address = (host, int(port))
request = 'GET /' + filename + ' HTTP/1.1\\r\\n'
host = 'Host: ' + url[0] + '\\r\\n'
blank_line = "\\r\\n\\"
header = request + '\n' + host + '\n'

if os.path.isfile(filename.split('.')[0] + '.cache'):
    secs = os.path.getmtime(filename.split('.')[0] + '.cache')
    t2 = time.gmtime(secs)
    last_mod = time.strftime("%a, %d %b %Y %H:%M:%S GMT\\r\\n", t2)
    header += 'If-Modified-Since: ' + last_mod +'\n'

header+= blank_line + '\n'

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(header)

try:
    clientsocket.connect(address)
    clientsocket.sendall(header.encode())
    data = b''
    while True:
        buff = clientsocket.recv(1024)
        if not buff:
            break
        data += buff
    clientsocket.close()
    data = data.decode()
    headers_array = data.split("\n")

    headers = ""
    for item in headers_array[:6]:
            headers += item
            headers += "\n"
    print(headers)

    content = ""
    if headers_array[0].split(" ")[1] == "200":
        for item in headers_array[6:]:
            content += item
        fin = open(filename.split('.')[0] + '.cache', "w+")
        fin.write(content)
        fin.close()

    elif headers_array[0].split(" ")[1] == "304":
        content =""

    elif headers_array[0].split(" ")[1] == "404":
        content = ""

    print(content)
    clientsocket.close()
        
except socket.timeout as e:
    print('\nRequest attempt timed out')

except OSError as e:
    print('\nRequest attempt timed out (with an error)')
