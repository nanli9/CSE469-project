#!/usr/bin/python3
from datetime import datetime
import os
import os.path
import struct
import hashlib
import datetime
import time
from decimal import Decimal
import sys

# Path to check the blockchain file

if not ("BCHOC_FILE_PATH" in os.environ):
    os.environ["BCHOC_FILE_PATH"] = "bchoc_file.bin"

file_path = os.environ["BCHOC_FILE_PATH"]
# we need to implement these functions


def append(case_id, item_list, ip_state="CHECKEDIN", data_length=0,message="Added item: ", info=""):
    # get prehash value
    bchoc_file_read = open(file_path, "rb")
    data = bchoc_file_read.read()
    index = 0
    length = 0
    while index <= (len(data) - 1):
        length = struct.unpack("I", data[index + 72 : index + 76])[0]
        index = index + length + 76
    bchoc_file_read.close()
    pre_sha256 = bytes.fromhex(hashlib.sha256(data[index - length - 76 :]).hexdigest())
    # print(pre_sha256)
    # print(pre_sha256.hex())

    bchoc_file = open(file_path, "ab")
    print("Case: ", case_id)
    for i in item_list:
        dt = datetime.datetime.now()
        time_stamp = dt.timestamp()
        item_id = int(i)
        state = bytes(ip_state, "utf-8")
        packed_data = struct.pack(
                "32sd16sI12sI",
                pre_sha256,
                time_stamp,
                bytes(case_id, "utf-8"),
                item_id,
                state,
                int(data_length),
            )
        bchoc_file.write(packed_data)
        # print(type(packed_data))
        print(message,i)
        #unpacked_data = str(pre_sha256)+str(time_stamp)+str(bytes(case_id,"utf-8"))+str(item_id)+ip_state+str(data_length)
        pre_sha256=bytes.fromhex(hashlib.sha256(packed_data).hexdigest())
        #unpacked_data = bytes(unpacked_data,"utf-8")
        #pre_sha256 = bytes.fromhex(
           # hashlib.sha256(unpacked_data).hexdigest()
        #)
        #print(pre_sha256.hex())
        print(f"  Status: {ip_state}")
        if(info!=""):
            bchoc_file.write(bytes(info, "utf-8"))
            print("  Owner info: ",info)
        print("  Time of action:",str(datetime.datetime.fromtimestamp(time_stamp)).replace(" ","T")+"Z")
    bchoc_file.close()


def checkout(item_id):
    bchoc_file = open(file_path, "rb")
    data = bchoc_file.read()
    listOfEntries = create_listOfItems(data)
    listOfEntries.reverse()
    item = getItem(listOfEntries, item_id)
    if not item:
        print("Error: Checkout failed,item does not exist")
        return 21
    status = item[2]
    case_id = item[0]
    # Error codes :
    # 2 -> checkout error
    #   1 : does not exist error
    #   2 : item already checkedout error
    #   3 : item already removed error
    if status:
        if status in ["RELEASED", "DISPOSED", "DESTROYED"]:
            print("Error: Cannot check out a removed item.")
            return 23
        elif status == "CHECKEDOUT":
            print("Error: Cannot check out a checked out item. Must check it in first.")
            return 22
        else:
            append(case_id, [item_id], ip_state = "CHECKEDOUT",message="Checked out item: ")
            return 0


def checkin(item_id):
    bchoc_file = open(file_path, "rb")
    data = bchoc_file.read()
    listOfEntries = create_listOfItems(data)
    listOfEntries.reverse()
    item = getItem(listOfEntries, item_id)
    if not item:
        print("Error: Checkin failed,item does not exist")
        return 11
    status = item[2]
    case_id = item[0]
    # Error codes :
    # 1 -> checkin error
    #   1 : does not exist error
    #   2 : item already removed error
    if status:
        if status in ["RELEASED", "DISPOSED", "DESTROYED"]:
            print("Error: Cannot check in a removed item.")
            return 12
        else:
            append(case_id, [item_id])
            return 0


def log(num_entries, ip_case_id, ip_item_id, reverse):
    # if num_entries is -1 then all log should be printed
    num_entries = int(num_entries)
    bchoc_file = open(file_path, "rb")
    data = bchoc_file.read()
    # print(len(data))
    listOfEntries = create_listOfItems(data)
    if reverse:
        listOfEntries.reverse()
    if num_entries == -1:
        num_entries = len(listOfEntries)

    for item in listOfEntries:
        if num_entries == 0:
            break
        if ip_item_id and int(item[1]) != int(ip_item_id):
            continue
        case_id = item[0]
        item_id = item[1]
        status = item[2]
        time_stamp = item[3]
        
        timeToShow = str(time_stamp).replace(" ","T")+"Z"
        print(
            f"Case: {case_id}\nItem: {item_id}\nAction: {status}\nTime: {timeToShow}\n\n"
        )
        num_entries -= 1

    bchoc_file.close()


def create_listOfItems(data):
    index = 0
    listOfEntries = []
    while index <= (len(data) - 1):
        # pre hash value
        # print(struct.unpack("32s", data[index : index + 32])[0])
        pre_hash=(struct.unpack("32s", data[index + 0 : index + 32])[0]).hex()
        dateTime = datetime.datetime.fromtimestamp(
            struct.unpack("d", data[index + 32 : index + 40])[0]
        )
        case_id = (
            str(struct.unpack("16s", data[index + 40 : index + 56])[0])
            .split("\\x")[0]
            .split("'")[1]
        )
        item_id = struct.unpack("I", data[index + 56 : index + 60])[0]
        status = (
            str(struct.unpack("12s", data[index + 60 : index + 72])[0])
            .split("\\x")[0]
            .split("'")[1]
        )
        length = struct.unpack("I", data[index + 72 : index + 76])[0]
        cur_hash=hashlib.sha256(data[index:index+76+length]).hexdigest()
        index = index + length + 76
        # print("len: ", length)
        # print("index: ", index)
        listOfEntries.append((case_id, item_id, status, dateTime,pre_hash,cur_hash,length))
        
    return listOfEntries


def getItem(listOfEntries, item_id):
    for item in listOfEntries:
        if int(item[1]) == int(item_id):
            return item
    return None


def remove(item_id, reason,owner):
    #print(item_id)
    #print(reason)
    #print(owner)
    bchoc_file_read = open(file_path, "rb")
    data = bchoc_file_read.read()
    case_id=(struct.unpack('16s',data[130:146])[0]).decode("utf-8")
    append(case_id,[item_id],reason,len(owner),"Removed item",owner)


def init():
    if os.path.exists(file_path) == False:
        print("Blockchain file not found. Created INITIAL block.")
        dt = datetime.datetime.now()
        time_stamp = dt.timestamp()
        # print(time_stamp)
        pre_hash = bytes("None", "utf-8")
        case_id = bytes("None", "utf-8")
        item_id = bytes("None", "utf-8")
        state = bytes("INITIAL", "utf-8")
        data_length = format(14, "b")
        data = bytes("Initial block", "utf-8")
        bchoc_file = open(file_path, "ab")
        bchoc_file.write(
            struct.pack("32sd16sI12sI", pre_hash, time_stamp, case_id, 0, state, 14)
        )
        bchoc_file.write(data)
        bchoc_file.write(b"\0")
        bchoc_file.close()
    else:
        print("Blockchain file found with INITIAL block.")


def verify():
    print("verify")
    #31:missing parent, 32:same parent, 33:unmatch checksum,34:transactions after remove
    error_code=0
    bchoc_file_read = open(file_path, "rb")
    data = bchoc_file_read.read()
    bad_block_index=0
    block_info=create_listOfItems(data)[0:]
    length=len(block_info)
    for block in block_info :    
        print(block[1]," : ",block[4], " : ",block[5],"\n")
    errorFound = False
    removedItems = []
    for i in range(len(block_info)):
        if errorFound :
            break

        # cur_hash=hashlib.sha256(
        #     (str(block_info[i][4])+str(block_info[i][3])+str(block_info[i][0])+str(block_info[i][1])+str(block_info[i][2])+str(block_info[i][6]))
        #     .encode()).hexdigest()
            
        if block_info[i][2] in ["RELEASED", "DISPOSED", "DESTROYED"]:
            removedItems.append(block_info[1])
            
        elif block_info[i][2] in ["CHECKEDIN", "CHECKEDOUT"] :
            if block_info[i][2] in removedItems :
                error_code=34
                bad_block_index=i
                break
        
        
        # print("curr_hash: ",block_info[i][4])
        # print("pre_hash: ",block_info[i][4])
        for j in range(i+1,len(block_info)):          
            if block_info[i][4]==block_info[j][4]:
                error_code=31
                bad_block_index=j
                errorFound = True
                break
            
            
            if block_info[i][5]!=block_info[j][4]:
                error_code=32
                bad_block_index=j
                errorFound = True
                break 
                            
        # print("cur_hash: ", block_info[i][5])
    # print(error_code)
    print("Transactions in blockchain: ",length)
    if(error_code==0):
        print("State of blockchain: CLEAN")
        return 0
    elif error_code==31:
        print("State of blockchain: ERROR")
        print("Bad block: ",block_info[bad_block_index])
        print("Parent block: ",block_info[bad_block_index-1])
        print("Two blocks were found with the same parent.")
        return 31
    elif error_code==32:
        print("State of blockchain: ERROR")
        print("Bad block: ",block_info[bad_block_index])
        print("Parent block: NOT FOUND")
        return 32
    elif error_code==33:
        print("State of blockchain: ERROR")
        print("Bad block: ",block_info[bad_block_index])
        print("Block contents do not match block checksum.")
        return 33
    
    elif error_code==34:
        print("State of blockchain: ERROR")
        print("Bad block: ",block_info[bad_block_index])
        print("Item checked out or checked in after removal from chain.")
        return 34
    


# parse the input

inputArray = sys.argv
# print(sys.argv)
if inputArray[0] == "./bchoc":
    # add commands
    if inputArray[1] == "add":
        # print("perform add command")
        if inputArray[2] == "-c":
            case_id = inputArray[3]
            # bchoc_file.write(bytes(case_id,'utf-8'))
            item_list = []
            for i in range(4, len(inputArray), 2):
                # print("another item")
                if inputArray[i] == "-i":
                    item_list.append(inputArray[i + 1])
                    # bchoc_file.write(inputArray[i + 1])
                else:
                    sys.exit(1)
            # print(item_list)
            append(case_id, item_list)
        else:
            sys.exit(1)
    # checkout command
    elif inputArray[1] == "checkout":
        # print("perform checkout command")
        if len(inputArray) == 4 and inputArray[2] == "-i":
            item_id = inputArray[3]
            # call checkout command here
            exit_code = checkout(item_id)
        if exit_code:
            sys.exit(exit_code)
    elif inputArray[1] == "checkin":
        # print("perform checkin command")
        if len(inputArray) == 4 and inputArray[2] == "-i":
            item_id = inputArray[3]
            # call checkin command here
            exit_code = checkin(item_id)
            if exit_code:
                sys.exit(exit_code)

    elif inputArray[1] == "log":
        num_entries = -1
        case_id = ""
        item_id = ""
        reverse = False
        for i in range(len(inputArray)):
            if inputArray[i] == "-n":
                num_entries = inputArray[i + 1]
            if inputArray[i] == "-c":
                case_id = inputArray[i + 1]
            if inputArray[i] == "-i":
                item_id = inputArray[i + 1]
            if inputArray[i] == "-r":
                reverse = True
        log(num_entries, case_id, item_id, reverse)
    elif inputArray[1] == "remove":
        #print("perform remove command")
        # call remove command here
        item_id = inputArray[3]
        reason = inputArray[5]
        owner = ""
        if len(inputArray) > 6:
            owner = inputArray[7]
        exit_code = remove(item_id, reason,owner)
        if exit_code :
            sys.exit(1)
    elif inputArray[1] == "init":
        # call the Linked list constructor to check the LL or create intial block
        init()
    elif inputArray[1] == "verify":
        print("perform verify command")
        # call verify command here
        exit_code = verify()
        if exit_code:
                sys.exit(exit_code)
    else:
        sys.exit(1)
else:
    sys.exit(1)

# pack the data should be stored in bchoc
