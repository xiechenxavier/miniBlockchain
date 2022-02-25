#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 18:23:31 2022

@author: xiechen
"""

from hashlib import sha256
# import time
import datetime;
 

class Block:

    def __init__(self, index, data, timestamp, preHash = ""):
        self.index = index
        self.data = data
        self.timestamp = timestamp
        self.nounce = 0
        self.preHash = preHash
        self.hash = self.calculateHash()
        self.MerkleRoot = self.calculMerkleRoot()

    def calculateHash(self):
        resultData = str(self.index) + str(self.data) + str(self.timestamp) + str(self.nounce)
        return sha256(resultData.encode("utf-8")).hexdigest()

    #挖矿，difficulty代表复杂度，也就是计算所得HASH前difficulty位必须为0
    def minerBlock(self,difficulty):
        while(self.hash[0:difficulty] != str(0).zfill(difficulty)):
            self.nounce = self.nounce + 1
            self.hash = self.calculateHash()
            
    def calculMerkleRoot(self):
        if not(self.data is None) or len(self.data) ==0:
            return sum([hash(ele) for ele in self.data])
        else:
            return 0
        
    def Transactions_hashval(self):
        
        return [hash(trans) for trans in self.data]

    def __str__(self):
        return str(self.__dict__)

class Blockchain:

    def __init__(self):
        self.chain = [self.createGenesisBlock()]
        self.difficulty = 5

    def createGenesisBlock(self):
        ts = datetime.datetime.now().timestamp()
        return Block(0,"genesis block", ts)

    def getLastBlock(self):
        return self.chain[len(self.chain) - 1]

    #添加区块，添加前还需要一道计算题minerBlock()
    def addBlock(self, newBlock):
        newBlock.preHash = self.getLastBlock().hash
        newBlock.minerBlock(self.difficulty)
        self.chain.append(newBlock)

    def __str__(self):
        return str(self.__dict__)

    def chainIsValid(self):
        for index in range(1,len(self.chain)):
            currentBlock = self.chain[index]
            preBlock = self.chain[index - 1]
            if(currentBlock.hash != currentBlock.calculateHash()):
                return False
            if(currentBlock.preHash != preBlock.hash):
                return False
        return True


