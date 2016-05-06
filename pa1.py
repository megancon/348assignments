#Megan Conlon
#mac357

#Problem 1

def binarySearch(L,v): 
	""" checks whether a value v is in a sorted list L"""

	size = len(L)
	n = 0 #number of iterations
	mini= 0 # position of the first number in the sorted list
	maxi = size-1	#position of the last number in the sorted list
	t = False


	while mini <= maxi and t == False:
		mid = (mini+maxi)/2
		if v == L[mid]:
			t = True
			return (t, n)
		elif v > mid:
			mini = mid + 1
		else:
			maxi = mid - 1
		n+=1
	return (t, n)


#Problem 2:

def mean(L):
	""" return the average of a list of numbers"""
	if len(L) == 0:
		return 0
	return float(sum(L))/float (len(L))

def median (L):
	"""return the median of a list of numbers"""
	size = len(L)

	if size == 0:
		return 0
	midpt = (size-1) / 2
	L.sort()
	if (size % 2) == 0: 	#if there is an odd number of items in the list
		ci1 = L[midpt]
		ci2 = L[midpt +1]
		return (float(ci1) + float(ci2))/2		#average the two central items
	return float(L[midpt])		#otherwise return the middle item


# Problem 3

def bfs (tree, elem):
	"""perform a breadth first search of the tree and return whether or not 'elem' is in 'tree'"""


	q = [(tree[0])]		#initialize q with the root
	checklst = [tree[1:]] 	#store the rest of the tree to be checked

	while len(q)>0:
		curr = q.pop()		#current node to be checked
		kids = checklst.pop() #store the children of the node
		print curr

		if (curr == elem):
			return True
		for item in kids:
			q.insert(0, item[0])		#insert the first leaf into the first position of the queue
			checklst.insert(0,item[1:])		#insert the rest of the leaves into the list of integers to be checked 
	return False

def dfs (tree, elem):
	"""perform a depth first search of the tree and return whether or not 'elem' is in 'tree'"""
	
	q = [(tree[0])]		#initialize q with the root
	checklst = [tree[1:]]	#store the rest of the tree to be checked

	while len(q)>0:
		curr = q.pop()
		kids = checklst.pop()
		print curr

		if (curr == elem):
			return True
		for item in kids:
			q.append(item[0])		#append the first leaf to the end of the queue
			checklst.append(item[1:])	#append the rest of the leaves to the end of the list to be checked 
	return False


#Problem 4

class TTTBoard: 
	"""class for managaing a game of Tic Tac Toe"""

	def __init__(self):	
		""" initialize a 3 x 3 tic tac toe board"""
		self.lst = ["*","*","*","*","*","*","*","*","*"]

	def __str__(self):
		""" returns a string representation of the tic tac toe board"""
		return str(self.lst[0]) + " " + str(self.lst[1]) + " " + str(self.lst[2]) + "\n" + str(self.lst[3]) + " " + str(self.lst[4]) + " " + str(self.lst[5]) + "\n" + str(self.lst[6]) + " " + str(self.lst[7]) + " " + str(self.lst[8])

	def makeMove(self, player,pos):
		""" places a move for player in the position pos, returns True if the move was made and False if not"""
		if self.lst[pos] == "*" and 0 <= pos <=9:
			self.lst[pos] = player
			return True
		return False

	def hasWon(self, player):
		""" returns True if a player has won the game, and False if not"""
		if self.lst[0] == player and self.lst[1] == player and self.lst[2] == player:	#checks first row
			return True
		if self.lst[3] == player and self.lst[4] == player and self.lst[5] == player:	#checks second row
			return True
		if self.lst[6] == player and self.lst[7] == player and self.lst[8] == player:	#checks third row
			return True
		if self.lst[0] == player and self.lst[3] == player and self.lst[6] == player:	#checks first column
			return True
		if self.lst[1] == player and self.lst[4] == player and self.lst[7] == player:	#checks second column
			return True
		if self.lst[2] == player and self.lst[5] == player and self.lst[8] == player:	#checks third column
			return True
		if self.lst[0] == player and self.lst[4] == player and self.lst[8] == player:	#checks first diagonal
			return True
		if self.lst[2] == player and self.lst[4] == player and self.lst[6] == player:	#checks second diagonal
			return True
		return False

	def gameOver(self):
		""" returns True if player has won the game, and False if not"""
		if self.hasWon == True:
			return True	
		for item in self.lst:
			if item != "*":		#if there are no *'s (empty spaces) left
				return True
		return False

	def clear(self):
		""" clears the board to reset the game"""
		self.lst = ["*","*","*","*","*","*","*","*","*"]


			

