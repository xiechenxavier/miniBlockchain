#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 11:57:08 2022

@author: xiechen
"""


import socket
import sys
import threading
import time


class Wallet:
    
    def __init__(self, Adr, Port):
        
        self.adr = Adr
        self.port = Port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def send_Trans_to_Miner(self, Miner_adr, miner_port, mode):
        
        # address of destination
        miner = (str(Miner_adr), int(miner_port))
        self.sock.bind((str(self.adr), int(self.port)))
        
        PreLabel = ''
        End_pair = ''
        if mode == 'inform transaction':
            
            PreLabel = '#Information*'
            
        elif mode == 'check transaction':
            
            PreLabel = '#Verification*'
            End_pair = '%from%Client' + str(self.adr) +'_'+ str(self.port)
            
        while True:
            
                if(mode == 'check transaction'):
                    print("\nPlease input a transaction to check.")
                # 'B is going to send money to F'
                message = input('. . . @@: ')
                if 'exit' in message:
                    break
                else:
                    self.sock.sendto((PreLabel +message + End_pair).encode(), miner)
                
                time.sleep(0.1)
    
    def getFeedBack_from_Miner(self):
        
        while True:
            data = self.sock.recv(1024).decode()
            print(data)
            # time.sleep(0.3)
    
    # def testFunction(self):
        

if len(sys.argv) < 2:
    print('please set port of wallet and mode of function(tape 0/1)')
# main function for test part          
loc_ip = '0.0.0.0'
loc_port = int(sys.argv[1])
# sock.bind((loc_ip, loc_port))
wal = Wallet(loc_ip, loc_port)
Miner_adr = input('Input a miner address:\n')
miner_port = input('Input its port:\n')


mode = sys.argv[2]

if int(mode) == 1:
    wal.send_Trans_to_Miner(Miner_adr, miner_port, 'inform transaction')
elif int(mode) == 0:
    sen_thread = threading.Thread(target=
                                  wal.send_Trans_to_Miner, args=(Miner_adr, 
                                                          miner_port, 
                                                          'check transaction'))
    rec_thread = threading.Thread(target=wal.getFeedBack_from_Miner)
    
    sen_thread.start()
    rec_thread.start()
    
    sen_thread.join() # join的目的：让一个先运行，一个后运行
    rec_thread.join()
    
else:
    print('mode error, you should set 0 or 1')


