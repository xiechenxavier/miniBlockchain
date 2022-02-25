# miniBlockchain
Tutorial Blockchain project at school.
That's a project assigned by teacher, which merely shows an implementatioin of a basical mini-blockchain with P2P network and UDP transmission.
If you'd like to try it on your PC.

First, executing the Server by typing:

- python Server.py

And executing several different miners via different terminals:

- python Miner.py '[port]'

Executing a wallet with its 1st mode:  send transactions to one of miners:

- python Wallet.py '[port]' 1
Input the address and ip of a Miner to send

Executing another wallet with its 0th mode: check the validity of one transaction.
Input the address and ip of a Miner to consult
