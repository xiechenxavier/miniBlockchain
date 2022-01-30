#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 15:17:48 2022

@author: xiechen
"""


import socket
import threading
import time

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddress = ('192.168.43.181', 11111)

#recvfrom()函数：
#接收UDP数据，与recv()类似，但返回值是（data,address）。
#其中data是包含接收的数据，address是发送数据的套接字地址。

#连接服务器
chain = input('连接口令：') 
send = ('#connectChain*'+chain).encode()
s.sendto(send, serverAddress)# send "#connectChain*"+token
message = eval(s.recvfrom(2048)[0].decode())
myPeer = message[0] # 受到了address
signature = str(message[1])  #这个是signature 端口号
print('got myPeer: ', myPeer)

peerConnected = False
#先连接myPeer，再互发消息
# firstly, it send its own signature to peer in order to verify 
# whether it's connected
# secondly, if it's already connected, it will start to send message.
def sendToMyPeer():
    #发送包含签名的连接请求
    global peerConnected
    while True:
        s.sendto(signature.encode(), myPeer)
        if peerConnected:
            break
        time.sleep(1)
    
    #发送聊天信息
    while True:
        send_text = input("我方发送：")
        s.sendto(send_text.encode(), myPeer)

def recFromMyPeer():
    #接收请求并验证签名or接收聊天信息
    global peerConnected
    while True:
        message = s.recvfrom(2048)[0].decode()
        if message == signature: # 如果要连接验证签名
            if not peerConnected: #若还没有连接成功
                print('connected successfully') #表明连接成功
            peerConnected = True #并且更新变量peerConnected
        elif peerConnected: # 如果已经连接
            print('\r对方回复：'+message+'\n我方发送：', end='') #相当于是交流信息

sen_thread = threading.Thread(target=sendToMyPeer)
rec_thread = threading.Thread(target=recFromMyPeer)

sen_thread.start()
rec_thread.start()

sen_thread.join() # join的目的：让一个先运行，一个后运行
rec_thread.join()