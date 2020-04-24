# Shuo Zhang
# 21801147
# Section 102
#! /usr/bin/env python3
# HTTP Server

import sys
import socket
import datetime, time
import os.path

serverip = sys.argv[1]
serverport = int(sys.argv[2])
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((serverip, serverport))
serversocket.listen(1)
count = 0

while True:
    connectionSocket, address = serversocket.accept()
    data = connectionSocket.recv(10000).decode()
    headers_array = data.split("\n")
    get_header = headers_array[0].split(' ')
    file_name = get_header[1].split('/')[1]

    time_now = datetime.datetime.now(datetime.timezone.utc)
    time_now = "Date: " + time_now.strftime("%a, %d %b %Y %H:%M:%S GMT\\r\\n\n")

    response = ""

    requested_fresh = False

    if os.path.isfile(file_name):

        res_time = os.path.getmtime(file_name)
        res_file_time = time.gmtime(res_time)
        last_mod_time = time.strftime("%a, %d %b %Y %H:%M:%S GMT\\r\\n", res_file_time)

        has_modified_header = False
        moddedtime = ""

        for item in headers_array:
            if item.split(" ")[0] == 'If-Modified-Since:':
                has_modified_header = True
                moddedtime = item[19:]

        if has_modified_header:
            old = time.strptime(moddedtime, "%a, %d %b %Y %H:%M:%S %Z\\r\\n")
            old_time = time.mktime(old)
            new_time = time.mktime(res_file_time)

            if new_time > old_time:
                response = "HTTP/1.1 200 OK\\r\\n\n"
                requested_fresh = False
            else:
                response = "HTTP/1.1 304 Not Modified\\r\\n" + '\n'
                requested_fresh = True
        else:
            response = "HTTP/1.1 200 OK\\r\\n\n"
        
        response += time_now

        if requested_fresh == True:
            response += "\\r\\n"
        else:
            fin = open(file_name, "r")
            contents = fin.read()
            fin.close()

            response += 'Last-Modified: ' + last_mod_time
            response += "\nContent-Length: " + str(len(contents)) + "\\r\\n"
            response += "\nContent-Type: text/html; charset=UTF-8\\r\\n"
            response += '\n\\r\\n\n'
            response += contents
    else:
        response = "HTTP/1.1 404 Not Found\\r\\n\n"
        response += time_now
        response += "Content-Length: 0" + "\\r\\n\n"
        response += "\\r\\n\n"
    connectionSocket.send(response.encode())
    connectionSocket.close()