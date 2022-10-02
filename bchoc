#!/usr/bin/python3
import struct
#self define node class
class Node(object):
	def __init__(self):
		self.data = None # contains the data
		self.next = None # contains the reference to the next node
		#the data should be pack in 32s d 16s I 12s I
		#self.blockData=struct.pack('32s d 16s I 12s I')

#a skeleton of bchoc we should implement it in more detail
class LinkedList:
	def __init__(self):
		self.head = None

	def append(self, data):
		new_node = Node() # create a new node
		new_node.data = data
		if(self.head==None):
			self.head = new_node
		else:
			temp_node=self.head
			while temp_node.next:
				temp_node=temp_node.next
			temp_node.next=new_node
	def reverse(self):
		temp_node=self.head
	def remove(self,data):
		temp_node=self.head
	def list_print(self):
		node = self.head # cant point to ll!
		while node:
			print(node.data)
			node = node.next
#take the inputs
input = input();
#split input by space 
inputArray=input.split(" ")
print(inputArray)
#all the following code are just test for pack and the linkedlist
print(struct.pack('4s',bytes(inputArray[1], 'utf-8')))
ll = LinkedList()
ll.append(1)
ll.append(2)
ll.append(3)
ll.append(3)
ll.append(3)
ll.append(3)
ll.list_print()

