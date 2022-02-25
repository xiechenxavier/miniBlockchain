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
from Block import Block,Blockchain
from Node import Node, Arbre_Merkle
import time
import datetime

# address of server, 形式为(ipaddr，port)的元组
rendezvous = ('192.168.129.185', 55556)

# connect to rendezvous
print('connecting to rendezvous server')

#通过AF_INET设定网络协议为IPv4，且服务器之间网络通信，
#SOCK_DGRAM设置传输层使用UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#将套接字绑定到地址, 在AF_INET下,以元组(host,port)的形式表示地址.
loc_ip = '192.168.129.185'
loc_port = int(sys.argv[1])
sock.bind((loc_ip, loc_port))
#发送UDP数据。将数据发送到套接字，
# address是形式为(ipaddr，port)的元组，指定远程地址。返回值是发送的字节数。
sock.sendto(b'0', rendezvous)

peers = []
peers.append((loc_ip, loc_port)) # add itself
messages = []
# create local blockchain
myBlockChain = Blockchain()

def Server_ready():
    while True:
        # 接受TCP套接字的数据。数据以字符串形式返回，bufsize指定要接收的最大数据量。
        # message.decode() 也就是消息解码
        data = sock.recv(1024).decode()
    
        if data.strip() == 'ready':
            print('checked in with server, waiting')
            break

def dealwith_node_connected(data):
# concerning the received node's information, cur node needs to identify
# that's old node or new node
   data1 = data.replace('#The_miner:','')
   ip, sport = data1.split(' ')
   sport = int(sport)
       # get another peer's information
   if len(peers) < 2: # it means that received node is an old one, sent by server
       
       print('\ngot an old peer')
       print('  ip:          {}'.format(ip))
       print('  source port: {}'.format(sport))
       peers.append((ip,sport))
       sock.sendto('#hello {} {}'.format(loc_ip, loc_port).encode(), 
                   (ip, sport))
   else:
       print('\ngot a new peer to add:')
       print('  ip:          {}'.format(ip))
       print('  source port: {}'.format(sport))
       peers.append((ip,sport))

def Broadcast(peers,data,label):
    '''
    
    Parameters
    ----------
    data : Byte
        Encoded data will be sent to the given destination.
    dest : tuple of ip and port
        The destination of getting data packet.

    Returns
    -------
    None.

    '''
    if len(peers) > 1:
        for i in range(1,len(peers)):
            sock.sendto((label+data.decode()).encode(), peers[i])
            # sock.sendto('{} {}'.format(ip, int(sport)).encode(),peers[i])

def reception_newnode_broadcast(data):
    
    text,ip, sport = data.split(' ')
    print(text)
    print("new node",' ip   :{}'.format(ip),
          ' port: {}'.format(sport)," connected")
    # send all old nodes to the new node
    sock.sendto(('#nodelist:'+str(peers)).encode(),(ip,int(sport)))
    # if there more than 1 old nodes
    packet = '{} {}'.format(ip, int(sport)).encode()
    Broadcast(peers,packet,'#The_miner:')
    peers.append((ip,int(sport)))

def get_and_register_list_of_old_nodes(data):
    
    data1 = data.replace('#nodelist:','')
    print(data1)
    M = ast.literal_eval(data1)
    # for a new node itself, received all old nodes being needed to add
    if len(M) > 1: 
        for i in range(1,len(M)):
            peers.append(M[i])
            
def removedList(li,stri):
    if not(stri in li):
        return li
    else:
        li.remove(stri)
        return li
            
# creating_block = None # current creating/created object
            
def createBlock_broadcast(traslist,peers):
    
#here we need to create Block, firstly add the block to local blockchain
    length_chain = len(myBlockChain.chain)
    ts = datetime.datetime.now().timestamp()
    global creating_block 
    creating_block = Block(length_chain,traslist,ts)
    #broadcast the block to other nodes
    str_block = str(creating_block) # string block
    block_packet = str_block.encode() # encode block packet
    Broadcast(peers,block_packet,'')

def Wallet_transaction(data):
    
    data1 = data.replace('#Information*', '') # delete label
    print(data1)
    if('->' in data1):
        mess = data1.split('->')
    else:
        mess = [data1]    
    for mes in mess:
        messages.append(mes)
    # mining now in order to create block
    data2 = data1 + " propagated from fm1"
    packet = str(data2).encode()
    # 1. broadcast message to other nodes
    Broadcast(peers,packet,'') 
    #create a block and broadcast it
    createBlock_broadcast(mess,peers)
    
def deal_with_mess_of_1stMiner(data):
    
    data1 = data.replace(" propagated from fm1", '')
    print(data1)
    if('->' in data1):
        mess = data1.split('->')
    else:
        mess = [data1]
        
    for mes in mess:
        messages.append(mes)
    # collect new transaction in a block
    #create a block and broadcast it
    createBlock_broadcast(mess,peers)
    
    
def mining_task_buildblock_extend_chain(data):
    
# decode block
    dist_block = ast.literal_eval(data)
    length_chain = len(myBlockChain.chain)
    # check whether this block is already added
    if list(dist_block['data']) != myBlockChain.chain[length_chain-1].data:
        conv_block = Block(dist_block['index'],list(dist_block['data']),dist_block['timestamp'])
        conv_block.nounce = dist_block['nounce']
        conv_block.preHash = dist_block['preHash']
        conv_block.hash = dist_block['hash']
 
        verified = True
        
        # get transaction of block
        for transaction in list(dist_block['data']):
            # transaction = dist_block['data']
            # verify the content transaction in the received block
            if transaction in messages:
            # whether the transaction is in the messages list
                if not(creating_block is None):
                    if transaction in creating_block.data:
                        # whether the transaction is in the creating block
                        creating_block.data = removedList(creating_block.data, 
                                                          transaction)
            else:
                verified = False
                break
        
        if verified:
            print("add the received block successfully")
            myBlockChain.addBlock(conv_block)
            if len(creating_block.data) > 0:
                print('it\'s going to add the creating block')
                creating_block.index = conv_block.index + 1
                creating_block.preHash = conv_block.hash
                creating_block.hash = creating_block.calculateHash()
                myBlockChain.addBlock(creating_block)
        else:
            print("the received block is not valid")
            myBlockChain.addBlock(creating_block)
        
        print("打印区块链上各区块：")
        for aBlock in myBlockChain.chain:
            print("\n")
            print(aBlock)
    
def Verification_transaction(data):
    
    data0 = data.replace('#Verification*', '')
    data1 = data0.split('%from%Client')[0]
    ip_port = data0.split('%from%Client')[1]
    ip_cli = ip_port.split('_')[0]
    port_cli = ip_port.split('_')[1]
    # Node1 = Node('v1',hash(data1),None,None)
    verified = False
    for block in myBlockChain.chain:
        
        if data1 in block.data: # found this transaction
           List_hash = block.Transactions_hashval() # hash value list
           cur_tree = Arbre_Merkle(List_hash) # build the tree
           Node_trans = cur_tree.getANodeByHash(hash(data1)) # found node
           # trans_frere = cur_tree.findBrother(Node_trans) # found its brother
           calculated_value = cur_tree.calcule_result_freres(Node_trans)
           
           verified = (cur_tree.simple_verification(Node_trans) and
                           calculated_value == block.MerkleRoot)
           
           break
       
    # feedback of verification to the wallet client
    if verified:
        feedback = 'This transaction is successfully checked'
    else:
        feedback = 'This transaction is not normal'
    sock.sendto(feedback.encode(),(ip_cli,int(port_cli)))
    
def dealwith_various_data():

    while True:
        data = sock.recv(1024).decode()
        if data:
            if (data.startswith('#The_miner:')):
                
                dealwith_node_connected(data)
                
            elif (data.startswith('#hello')):
                # print('fuck your mom',data)
                reception_newnode_broadcast(data)
            
            elif (data.startswith('#nodelist:')):
                
                get_and_register_list_of_old_nodes(data)
            
            # message from wallet, print and broadcast
            elif data.startswith('#Information*'):
                
                Wallet_transaction(data)
                
            # message from first noticed miner
            elif(" propagated from fm1" in data): # transactions from other nodes
                
                deal_with_mess_of_1stMiner(data)
            
            elif('#Verification*' in data):
                
                Verification_transaction(data)
                
            elif("nounce" in data): # it's a block
                
                mining_task_buildblock_extend_chain(data)

                
            
Server_ready()
dealwith_various_data()


            
               # # verify whether got a block from other nodes
                
               #  # add into local chain, because of the local acceptance
               #  myBlockChain.addBlock(creating_block) 
            
    

