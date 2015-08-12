"""add a docstring"""

#author: Peter Elliott
#email: pelliott@ualberta.ca
#date created: 6/7/2015

import random
import time

class Node:
	"""node object stores: coords, cumulative distance, if it has been visited, parent node, and neighbors' ids"""
	NODE = 0
	RELAY = 1
	SENSOR = 2
	SINK = 3
	UNCONNECTED = 4
	def __init__(self,x,y,t):
		"""creates new node at coordinates(x,y) with type t"""
		self.visited = False
		self.edges=[]
		self.X=x;
		self.Y=y;
		self.dist = float("inf")
		self.path = -1
		self.type = t
	def setPath(self,n):
		"""sets the next step that the data will take to an array index"""
		self.path = n
	
	def addEdge(self,id):
		"""adds the id to the list of nodes"""
		self.edges.append(id)
	def visit(self):
		"""marks the node as visited, so that it's distance is final"""
		self.visited = True
	def setType(self,t):
		"""can be used to change the type of a node"""
		self.type = t
	def distance(self,node):
		"""returns the euclidean distance of"""
		y = node.Y - self.Y
		x = node.X - self.X
		return ((y**2)+(x**2))**(0.5)
	def setDistance(self, d):
		"if d is less than current distance, d becoems the new current distance"
		if d<self.dist: 
			self.dist = d
			return True
		else:
			return False
	def printCoords(self):
		"""prints the x and y coord"""  
		print("(", self.X, ",", self.Y, ")")	

def addNode(nodes,seed,x,y,t):
	"""adds random node to list recursivly. this functions only purpose is to serve generateNodes()"""
	points = [[0,0]]
	for node in nodes:
		points.append([node.X,node.Y])
	X = random.randint(0,x)
	Y = random.randint(0,y)
	if [X,Y] not in points:
		nodes.append(Node(X,Y,t))
		return nodes
	else:
		return addNode(nodes,seed,x,y,t)

def generateNodes(n,seed,x,y): 
	"""creates n nodes within x:[0,x] and y:[0,y]. seed initializes random number generation."""
	random.seed(seed)
	nodes = [Node(0,0,Node.SINK)]
	for z in range(1,n):
		nodes = addNode(nodes,seed,x,y,Node.RELAY)
	return nodes

def setOuter(nodes):
	"""sets all outer nodes to sensors and all un connected nodes to unconnected"""
	paths = []
	for node in nodes:
		paths.append(node.path)
	for n in range(0,len(nodes)):
		if n not in paths and nodes[n].type != Node.SINK:
			if nodes[n].path != -1:
				nodes[n].setType(Node.SENSOR)
			else:
				nodes[n].setType(Node.UNCONNECTED)
	return nodes

def concentrate(*args):
	"""combines multiple arrays into one."""
	nodes = []
	for arg in args:
		nodes.extend(arg)
	return nodes


def getEdges(nodes, Range):
	"""initializes edges between nodes in array (nodes). range specifies the distance possible for a connection. """
	for current in range(0,len(nodes)):
		for x in range(0,len(nodes)):
			if nodes[current].distance(nodes[x]) <= Range:
				if x not in nodes[current].edges and current != x:
					nodes[current].addEdge(x)
	return nodes
	
def dijkstra(nodes,Range,cost):
	"""uses dijkstras algorithm to find the best path from nodes[0] to every other node. cost can be: "hop", "dist", "energ\""""
	nodes = getEdges(nodes,Range)
	current = 0
	nodes[current].setDistance(0)
	queue = []
	while True:
		for point in nodes[current].edges:
			if nodes[point].visited == False and nodes[current].type != Node.SENSOR:
				if cost == "dist":
					newMin = nodes[point].setDistance(nodes[current].distance(nodes[point]) + nodes[current].dist)
				elif cost == "hop":
					newMin = nodes[point].setDistance(1 + nodes[current].dist)
				if newMin:
					nodes[point].setPath(current)
				if point not in queue:
					queue.append(point)
		nodes[current].visit()
		position = 0
		minimum = float('inf')
		for p in range(0,len(queue)):
			if nodes[queue[p]].dist < minimum:
				minimum = nodes[queue[p]].dist
				position = p
		if len(queue) > 0:
			current = queue.pop(position)
		else:
			break
	return nodes


def getPath(nodes, n , arr):
	"""recursivly gets path back to source. arr should always be initialized with []."""
	if (nodes[n].X != 0 or nodes [n].Y != 0) and n != -1:
		arr.append(n)
		return getPath(nodes,nodes[n].path,arr)
	elif n == -1:
		arr.append("no connection")
		return arr
	else:
		arr.append(0)
		return arr


def sort(edges,nodes):
	"""sorts edges by highest amount of nodes. used by getSchedule()"""
	less = []
	equal = []
	greater = []

	if len(edges) > 1:
		pivot = len(nodes[edges[0][0]].edges)
		for x in edges:
			if len(nodes[x[0]].edges) < pivot:
				less.append(x)
			if len(nodes[x[0]].edges) == pivot:
				equal.append(x)
			if len(nodes[x[0]].edges) > pivot:
				greater.append(x)
		return sort(greater,nodes)+equal+sort(less,nodes)
	else:
		return edges


def overlap(a, b):
	"""checks for list overlap"""
	for i in a:
		if i in b:
			return True
	return False


def getSchedule(nodes):
	"""returns a list of paths from a list of nodes."""
	edges = []
	for p in range(0,len(nodes)):
		edges.append([p,nodes[p].path])
	edges = sort(edges, nodes)
	slots = []
	for p in edges:
		foundSlot = False;
		for q in range(0,len(slots)):
			if not overlap(nodes[p[0]].edges,slots[q]):
				samepath = False
				for z in slots[q]:
					if p[1] == nodes[z].path:
						samepath = True
				if not samepath and p[1] != -1: 
					foundSlot = True
					slots[q].append(p[0])
					break
				
		if not foundSlot and p[1] != -1:
			slots.append([p[0]])
	return slots

def formatNodeData(nodes,Range):
		f = []
		f.append("I i00 "+"{:0>2d}".format(nodes[0].X)+" "+"{:0>2d}".format(nodes[0].Y)+"\n")

		for z in range(1,len(nodes)):
			if nodes[nodes[z].path].type == Node.SINK:
				typ = "i"
			elif nodes[nodes[z].path].type == Node.RELAY:
				typ = "r"
			
			if nodes[z].type == Node.RELAY:
				f.append("R r"+"{:0>2d}".format(z)+" "+"{:0>2d}".format(nodes[z].X)+" "+"{:0>2d}".format(nodes[z].Y)+" "+str(Range)+" 0 0 "+typ+"{:0>2d}".format(nodes[z].path)+"\n")
			elif nodes[z].type == Node.SENSOR:
				f.append("S s"+"{:0>2d}".format(z)+" "+"{:0>2d}".format(nodes[z].X)+" "+"{:0>2d}".format(nodes[z].Y)+" "+str(Range)+" 0 0 "+typ+"{:0>2d}".format(nodes[z].path)+"\n")
		
		return f
	
	
	

	



