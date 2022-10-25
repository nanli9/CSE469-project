#!/usr/bin/python3
from datetime import datetime
import os
import struct
import hashlib
import time
import sys

# Path to check the blockchain file
os.environ["BCHOC_FILE_PATH "] = "."

#we need to implement these functions 
def append(case_id,item_list):
	print(case_id)
	print(item_list)

def checkout(item_id):
	print(item_id)

def checkin(item_id):
	print(item_id)
	
def log(num_entries,case_id,item_id,reverse):
	#if num_entries is -1 then all log should be printed
	print(num_entries)
	print(case_id)
	print(item_id)
	print(reverse)

def remove(item_id,reason,owner):
	print(item_id)
	print(reason)
	print(owner)
	
	
def init():
	print("init")
	
def verify():
	print("verify")
	

# parse the input
bchoc_file=open("bchoc_file.bin","ab")
inputArray = sys.argv
if inputArray[0] == "./bchoc":
    # add commands
    if inputArray[1] == "add":
        print("perform add command")
        if inputArray[2] == "-c":
            case_id = inputArray[3]
            #bchoc_file.write(bytes(case_id,'utf-8'))
            item_list = []
            for i in range(4, len(inputArray), 2):
                #print("another item")
                if inputArray[i] == "-i":
                    item_list.append(inputArray[i + 1])
                    #bchoc_file.write(inputArray[i + 1])
                else:
                    sys.exit(1)
            #print(item_list)
            append(case_id,item_list) 
        else:
            sys.exit(1)     
    # checkout command
    elif inputArray[1] == "checkout":
        print("perform checkout command")
        if len(inputArray) == 4 and inputArray[2] == "-i":
            item_id = inputArray[3]
            # call checkout command here
            checkout(item_id)
        else:
            sys.exit(1)
    elif inputArray[1] == "checkin":
        print("perform checkin command")
        if len(inputArray) == 4 and inputArray[2] == "-i":
            item_id = inputArray[3]
            # call checkin command here
            checkin(item_id)
        else:
            sys.exit(1)
    elif inputArray[1] == "log":
        num_entries=-1
        case_id=""
        item_id=""
        reverse=False
        for i in range(len(inputArray)):
            if(inputArray[i]=="-n"):
                num_entries=inputArray[i+1]
            if(inputArray[i]=="-c"):
                case_id=inputArray[i+1]
            if(inputArray[i]=="-i"):
                item_id=inputArray[i+1]
            if(inputArray[i]=="-r"):
                reverse=True
        log(num_entries,case_id,item_id,reverse)
    elif inputArray[1] == "remove":
        print("perform remove command")
        # call remove command here
        item_id=inputArray[3]
        reason=inputArray[5]
        owner=""
        if(len(inputArray)>6):
        	owner=inputArray[7]
        remove(item_id,reason,owner)
    elif inputArray[1] == "init":
        print("perform init command")
        # call the Linked list constructor to check the LL or create intial block
        init()
    elif inputArray[1] == "verify":
        print("perform verify command")
        # call verify command here
        verify()
    else:
        sys.exit(1)
else:
    sys.exit(1)
print(inputArray)
bchoc_file.close()
# pack the data should be stored in bchoc

