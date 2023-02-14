#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import sys
import socket
import struct
 
def send_and_receive_tcp(address, port, message):
    print("You gave arguments: {} {} {}".format(address, port, message))
    
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    tcp.connect((address, port))

    coded_message = message.encode()

    tcp.sendall(coded_message)

    data = tcp.recv(1024)

    data_string = data.decode()

    print('Recieved', data_string)

    tcp.close()

    split_data = data_string.split()
    
    cid = split_data[1]
    udp_port = split_data[2]
    
    send_and_receive_udp(address, port, cid, udp_port)
    return
 
 
def send_and_receive_udp(address, port, cid, udp_port):
    
    ACK = True
    EOM = False
    data_remaining = 0
    length = 19
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (address, int(udp_port))
    udp_message = ('Hello from ' + cid)
    
    print('Sending', udp_message)
    sending_data = struct.pack('!8s??HH128s', cid.encode(), ACK, EOM, data_remaining, length, udp_message.encode())
    udp.sendto(sending_data, server_address)
    
    while True:
	    while True:
	        udp_data, server = udp.recvfrom(1024)
	        break
	    recieved_data = struct.unpack('!8s??HH128s', udp_data)
	    EOM = recieved_data[2]
	    length = recieved_data[4]
	    full_message = recieved_data[5].decode()
	    message_wordlist = list(full_message)
	    recieved_list = []
	    for x in range(length):
	        character = message_wordlist[x]
	        recieved_list.append(character)
	    recieved_message = ''.join(recieved_list)
	    print('Recieved message:', recieved_message)
	    if (EOM == True):
	        break
	    split_message = recieved_message.split()
	    split_message.reverse()
	    sendable_message = ' '.join(split_message)
	    print('Sending message:', sendable_message)
	    sendable_data = struct.pack('!8s??HH128s', cid.encode(), ACK, EOM, data_remaining, length, sendable_message.encode())
	    udp.sendto(sendable_data, server_address)
    print('Exiting program...')
    udp.close()
    return
 
 
def main():
    USAGE = 'usage: %s <server address> <server port> <message>' % sys.argv[0]
 
    try:
        server_address = str(sys.argv[1])
        server_tcpport = int(sys.argv[2])
        message = str(sys.argv[3])
    except IndexError:
        print("Index Error")
    except ValueError:
        print("Value Error")
        sys.exit(USAGE)
 
    send_and_receive_tcp(server_address, server_tcpport, message)
 
 
if __name__ == '__main__':
    main()