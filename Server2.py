#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 15:15:26 2022

@author: xiechen
"""


import socket
import random

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 11111))

#记录口令信息
peers = {}

while True:
    message, address = s.recvfrom(2048)
    message = message.decode()
    if not message.startswith('#connectChain*'):
        continue
    chain = message.replace('#connectChain*', '')
    if chain not in peers: # 如果这是第一个连入的chain
        peers[chain] = address # keep this chain and peers[chain] = address
    else: #如果这个指令被记录
        print('matchedPeers: ', peers[chain], address) # matchedPeers
        verifySignature = random.randint(10000, 99999)  #签名验证,用于peers双方验证身份
        #给双方发送peer地址信息和签名
        s.sendto(str([peers[chain], verifySignature]).encode(), address)
        s.sendto(str([address,verifySignature]).encode(), peers[chain])
        peers.pop(chain) # 删掉chain
        
        
        
        