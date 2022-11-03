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


def append(case_id, item_list, ip_state="CHECKEDIN", message="Added item: "):
    # get prehash value
    bchoc_file_read = open(file_path, "rb")
    data = bchoc_file_read.read()
    index = 0
    length = 0
    while index <= (len(data) - 1):
        # print(
        #     datetime.datetime.fromtimestamp(
        #         struct.unpack("d", data[index + 32 : index + 40])[0]
        #     )
        # )
        length = struct.unpack("I", data[index + 72 : index + 76])[0]
        index = index + length + 76
        # print("len: ", length)
        # print("index: ", index)
    bchoc_file_read.close()
    pre_sha256 = hashlib.sha256(data[index - length - 76 :]).hexdigest()
    # print(pre_sha256)

    bchoc_file = open(file_path, "ab")
    print("Case: ", case_id)
    for i in item_list:
        pre_hash = bytes(pre_sha256, "utf-8")
        dt = datetime.datetime.now()
        time_stamp = dt.timestamp()
        item_id = int(i)
        state = bytes(ip_state, "utf-8")
        data_length = 0
        bchoc_file.write(
            struct.pack(
                "32sd16sI12sI",
                pre_hash,
                time_stamp,
                bytes(case_id, "utf-8"),
                item_id,
                state,
                data_length,
            )
        )
        print(message, i)
        print(
            f"  Status: {ip_state}\n  Time of action: ",
            datetime.datetime.fromtimestamp(time_stamp),
        )
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
            append(case_id, [item_id], "CHECKEDOUT", "Checked out item: ")
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
        dateTime = item[3]
        print(
            f"Case: {case_id}\nItem: {item_id}\nAction: {status}\nTime: {dateTime}\n\n"
        )
        num_entries -= 1

    # print("*************")
    # print(num_entries)
    # print(case_id)
    # print(item_id)
    # print(reverse)
    # a = struct.unpack("d", data[32:40])
    # timestamp = datetime.datetime.fromtimestamp(a[0])
    # print(timestamp)
    # print(struct.unpack("I", data[72:76])[0])
    bchoc_file.close()


def create_listOfItems(data):
    index = 0
    listOfEntries = []
    while index <= (len(data) - 1):
        # pre hash value
        # print(struct.unpack("32s", data[index : index + 32])[0])
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
        index = index + length + 76
        # print("len: ", length)
        # print("index: ", index)
        listOfEntries.append((case_id, item_id, status, str(dateTime)))
        # print(
        #     f"Case: {case_id}\nItem: {item_id}\nAction: {status}\nTime: {dateTime}\n\n"
        # )
    return listOfEntries


def getItem(listOfEntries, item_id):
    for item in listOfEntries:
        if int(item[1]) == int(item_id):
            return item
    return None


def remove(item_id, reason, owner):
    print(item_id)
    print(reason)
    print(owner)


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
        print("perform checkin command")
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
        print("perform remove command")
        # call remove command here
        item_id = inputArray[3]
        reason = inputArray[5]
        owner = ""
        if len(inputArray) > 6:
            owner = inputArray[7]
        remove(item_id, reason, owner)
    elif inputArray[1] == "init":
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

# pack the data should be stored in bchoc
