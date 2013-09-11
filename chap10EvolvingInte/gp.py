from random import random,randint,choice
from copy import deepcopy
from math import log

class fwrapper:
	def __init__(self,function,childcount,name):
		self.function=function
		self.childcount=childcount
		self.name=name

class node:
	def __init__(self,fw,children):
		self.function=fw.function
		self.name=fw.name
		self.children=children

	def evaluate(self,inp):
		results=[n.evaluate(inp) for n in self.children]
		return self.function(results)

class paramnode:
	def __init__(self,idx):
		self.idx=idx

	def evaluate(self,inp):
		return inp[self.idx]

class constnode:
	def __init__(self,v):
		self.v=v
	def evaluate(self,inp):
		return self.v

addw=fwrapper(lambda l:l[0]+l[1],2,'add')
subw=fwrapper(lambda l:l[0]-l[1],2,'subtract')
mulw=fwrapper(lambda l:l[0]*l[1],2,'multiply')

def iffunc(l):
	if l[0]>0:return l[1]
	else:return l[2]

ifw=fwrapper(iffunc,3,'if')

def isgreater(l):
	if l[0]>l[1]:return 1
	else:return 0

gtw=fwrapper(isgreater,2,'isgreater')

flist=[addw,mulw,ifw,gtw,subw]
