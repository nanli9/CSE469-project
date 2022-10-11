#!/usr/bin/python3
from datetime import datetime
import os
import struct
import hashlib
import time
import sys

# Path to check the blockchain file
os.environ["BCHOC_FILE_PATH "] = "."


# self define node class
class Node(object):
    def __init__(self):
        self.data = None  # contains the data
        self.next = None  # contains the reference to the next node
        # the data should be pack in 32s d 16s I 12s I
        # self.blockData=struct.pack('32s d 16s I 12s I')


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
        self.size = 1
        print("Blockchain file not found. Created INITIAL block.")

    def append(self, data):
        self.size += 1
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
        pre_node = self.head
        # if the list size is 2
        if self.size == 2:
            cur_node = pre_node.next
            cur_node.next = pre_node
            pre_node.next = None
            self.head = cur_node
        else:
            cur_node = pre_node.next
            next_node = cur_node.next
            next_node = self.head
            while cur_node.next:
                next_node = cur_node.next

    def remove(self, data):
        pre_node = self.head
        # if remove item is the head
        if pre_node.data == data:
            self.head = self.head.next
            pre_node.next = None
        # remove item is not in the head
        else:
            cur_node = pre_node.next
            while cur_node.data != data:
                pre_node = pre_node.next
                cur_node = pre_node.next
            # if the remove item is at the end of the list
            if cur_node.next == None:
                pre_node.next = None
            else:
                pre_node.next = cur_node.next
                cur_node.next = None

    def verify(self):
        temp_node = self.head

    def log(self):
        temp_node = self.head

    def list_print(self):
        node = self.head  # cant point to ll!
        while node:
            print(node.data)
            node = node.next

    def init(self):
        temp_node = self.head

    def checkin(self, item_id):
        temp_node = self.head

    def checkout(self, item_id):
        temp_node = self.head


# parse the input
input = input()
inputArray = input.split(" ")
if inputArray[0] == "bchoc":
    # add commands
    if inputArray[1] == "add":
        print("perform add command")
        if inputArray[2] == "-c":
            case_id = inputArray[3]
            item_list = []
            for i in range(4, len(inputArray), 2):
                print("another item")
                if inputArray[i] == "-i":
                    item_list.append(inputArray[i + 1])
                else:
                    sys.exit("wrong argument")
                    # call linkedlist add method here
            print(item_list)
        else:
            sys.exit("wrong argument")
            # checkout command
    elif inputArray[1] == "checkout":
        print("perform checkout command")
        if len(inputArray) == 4 and inputArray[2] == "-i":
            item_id = inputArray[3]
            # call checkout command here
        else:
            sys.exit("wrong argument")
    elif inputArray[1] == "checkin":
        print("perform checkin command")
        if len(inputArray) == 4 and inputArray[2] == "-i":
            item_id = inputArray[3]
            # call checkin command here
        else:
            sys.exit("wrong argument")
    elif inputArray[1] == "log":
        if len(inputArray) > 2:
            if inputArray[2] == "-r":
                print("log the reverse order")

        print("perform log command")
        # call log command here
    elif inputArray[1] == "remove":
        print("perform remove command")
        # call remove command here
    elif inputArray[1] == "init":
        print("perform init command")
        # call the Linked list constructor to check the LL or create intial block
        LinkedList()
    elif inputArray[1] == "verify":
        print("perform verify command")
        # call verify command here
    else:
        sys.exit("unexpected commands")
else:
    sys.exit("unexpected input format")
print(inputArray)

# pack the data should be stored in bchoc
# test for linkedlist methods
# print("test for linkedList method")
# ll.append(1)
# ll.append(2)
# ll.reverse()
# ll.list_print()
