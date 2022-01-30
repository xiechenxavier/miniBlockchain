#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 17:48:56 2022

@author: xiechen
"""
import socket
import sys
import threading
import ast

# address of server, 形式为(ipaddr，port)的元组
rendezvous = ('192.168.43.185', 55556)

# connect to rendezvous
print('connecting to rendezvous server')

#通过AF_INET设定网络协议为IPv4，且服务器之间网络通信，
#SOCK_DGRAM设置传输层使用UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#将套接字绑定到地址, 在AF_INET下,以元组(host,port)的形式表示地址.
loc_ip = '0.0.0.0'
loc_port = int(sys.argv[1])
sock.bind((loc_ip, loc_port))
#发送UDP数据。将数据发送到套接字，
# address是形式为(ipaddr，port)的元组，指定远程地址。返回值是发送的字节数。
sock.sendto(b'0', rendezvous)

peers = []
peers.append((loc_ip, loc_port)) # add itself
while True:
    # 接受TCP套接字的数据。数据以字符串形式返回，bufsize指定要接收的最大数据量。
    # message.decode() 也就是消息解码
    data = sock.recv(1024).decode()

    if data.strip() == 'ready':
        print('checked in with server, waiting')
        break

while True:
    data = sock.recv(1024).decode()
    if data:
        data_split = data.split(' ')
    # if data and not(isinstance(data.strip(),list)) and data.strip() != 'hello hehe':
        if len(data_split) == 2 and not("[" in data) and not("]" in data):
            # concerning the received node's information, cur node needs to identify
            # that's old node or new node
            ip, sport = data.split(' ')
            sport = int(sport)
                # get another peer's information
            if len(peers) < 2: # it means that received node is an old one, sent by server
                
                print('\ngot an old peer')
                print('  ip:          {}'.format(ip))
                print('  source port: {}'.format(sport))
                peers.append((ip,sport))
                sock.sendto('hello {} {}'.format(loc_ip, loc_port).encode(), 
                            (ip, sport))
            else:
                print('\ngot a new peer to add:')
                print('  ip:          {}'.format(ip))
                print('  source port: {}'.format(sport))
                peers.append((ip,sport))
            
        elif len(data_split) == 3:
            text,ip, sport = data.split(' ')
            print("new node",' ip   :{}'.format(ip),
                  ' port: {}'.format(sport)," connected")
            # send all old nodes to the new node
            sock.sendto((str(peers).encode()),(ip,int(sport)))
            # if there more than 1 old nodes
            if(len(peers) > 1):
                # inform other old nodes the new added node
                for i in range(1,len(peers)):
                    # peers[i] = tuple(peers[i][0],int(peers[i][1]))
                    sock.sendto('{} {}'.format(ip, int(sport)).encode(),peers[i])
            peers.append((ip,sport))
        
        elif ("[" in data):
            print(data)
            M = ast.literal_eval(data)
            # for a new node itself, received all old nodes being needed to add
            if len(M) > 1: 
                for i in range(1,len(M)):
                    peers.append(M[i])
    

