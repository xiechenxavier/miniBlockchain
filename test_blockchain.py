#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 12:54:50 2022

@author: xiechen
"""
# import os
from Block import Block,Blockchain
import time
import ast
import datetime

myBlockChain = Blockchain()

# 下面打印了每个区块挖掘需要的时间 比特币通过一定的机制控制在10分钟出一个块
# 其实就是根据当前网络算力 调整我们上面difficulty值的大小,如果你在
# 本地把上面代码difficulty的值调很大你可以看到很久都不会出计算结果

startMinerFirstBlockTime = time.time()
print("开始挖取第一个区块的时间：" + str(startMinerFirstBlockTime))

ts2 = datetime.datetime.now().timestamp()
block2 = Block(1,["第2个区块的交易数据在这里"],ts2)
print(block2.data)
myBlockChain.addBlock(block2)

startMinerSecondBlockTime = time.time()

print("挖取第二个区块耗费时间：" + str(startMinerSecondBlockTime - startMinerFirstBlockTime) + "s")

ts3 = datetime.datetime.now().timestamp()
myBlockChain.addBlock(Block(2,["第３个区块的交易数据在这里"],ts3))

print("挖取第三个区块耗费时间：" + str(time.time() - startMinerSecondBlockTime) + "s\n")

#打印
print("打印区块链上各区块：")
for aBlock in myBlockChain.chain:
    print("\n")
    print(aBlock)
    
str_block = str(myBlockChain.chain[1])
dist_block = ast.literal_eval(str_block)
# print(type(list(dist_block['data'])))
print('fuck transaction: ',dist_block['data'])
print(list(dist_block['data']))


print("\n")

#检查区块链有效性（是否被篡改）

#篡改前
print("篡改前区块链是否有效：\n")
print(myBlockChain.chainIsValid())

myBlockChain.chain[1].data = "我被篡改了"

#篡改后
print("篡改后区块链是否有效：\n")
print(myBlockChain.chainIsValid())


# print(hash())


