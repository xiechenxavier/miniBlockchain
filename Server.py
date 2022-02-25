#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 17:51:18 2022

@author: xiechen
"""

import socket

# known_port = 50010

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 55556))
clients = []

while True:

    while True:
        data, address = sock.recvfrom(128) # recv data and address

        print('connection from: {}'.format(address))
        clients.append(address) # add a new client to record #
        sock.sendto(b'ready', address)

        if len(clients) >= 2:
            break

        # if len(clients) == 2:
        #     print('got 2 clients, sending details to each')
        #     break

    curr_l = len(clients)
    c1 = clients[curr_l-1] # new client
    c1_addr, c1_port = c1
    c2 = clients[curr_l-2] # two der
    c2_addr, c2_port = c2

    # sock.sendto('{} {} {}'.format(c1_addr, c1_port, known_port).encode(), c2)
    # send the info of before last client to new client
    sock.sendto('#The_miner:{} {}'.format(c2_addr, c2_port).encode(), c1)

