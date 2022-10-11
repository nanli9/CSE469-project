#!/usr/bin/python3
from datetime import datetime
import os
import struct
import hashlib
import sys
import time

# Path to check the blockchain file
os.environ["BCHOC_FILE_PATH "] = "."

# self define node class
class Node(object):
    def __init__(self):
        # self.previousHash = None
        # self.timeStamp = None
        # self.caseID = None
        # self.evidenceItemID = None
        # self.stateOfItem = None
        # self.datLength = None
        # below fields will be packed using struct.pack() in metaData field

        self.metaData = None  # packed metadata -> previousHash,timeStamp,caseID,evidenceItemID,stateOfItem,datalength
        self.data = None  # contains the data
        self.next = None  # contains the reference to the next node

        # the data should be pack in 32s d 16s I 12s I
        # self.blockData=struct.pack('32s d 16s I 12s I')

    def __init__(
        self,
        metaData=None,
        data=None,
        next=None,
    ):
        self.metaData = metaData
        self.data = data
        self.next = next


# a skeleton of bchoc we should implement it in more detail
class LinkedList:
    def __init__(self):
        # TODO check file for blockchain

        # If file now found create intitial block
        data = str.encode("Initial block")
        current_timeStamp = time.time()
        stateOfItem = str.encode("INITIAL")
        dataLength = sys.getsizeof(data)
        metaData = self.getPackedInitialBlock(
            current_timeStamp, stateOfItem, dataLength
        )
        self.head = Node(
            metaData=metaData,
            data=data,
        )
        print("Blockchain file not found. Created INITIAL block.")

    def getPackedInitialBlock(self, current_timeStamp, stateOfItem, dataLength):
        return struct.pack(
            "d 12s I",
            current_timeStamp,
            stateOfItem,
            dataLength,
        )

    def append(self, data):
        new_node = Node()  # create a new node
        new_node.data = data
        if self.head == None:
            self.head = new_node
        else:
            temp_node = self.head
            while temp_node.next:
                temp_node = temp_node.next
            temp_node.next = new_node

    def reverse(self):
        temp_node = self.head

    def remove(self, data):
        temp_node = self.head

    def list_print(self):
        node = self.head  # cant point to ll!
        while node:
            print(node.data.decode())
            node = node.next


# initiating a blockchain and printing it
LinkedList().list_print()

# pack the data should be stored in bchoc
# test for linkedlist methods
# print("test for linkedList method")
# ll.append(1)
# ll.append(2)
# ll.reverse()
# ll.list_print()

# # take the inputs
# input = input()
# # split input by space
# inputArray = input.split(" ")
# print(inputArray)
# # all the following code are just test for pack and the linkedlist
# print(struct.pack("4s", bytes(inputArray[1], "utf-8")))
# ll = LinkedList()
# ll.append(1)
# ll.append(2)
# ll.append(3)
# ll.append(3)
# ll.append(3)
# ll.append(3)
# ll.list_print()
