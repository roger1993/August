import random

class Voter:
	def __init__(self, opinion):
		self.__opinion = opinion
		self.__friends = []

	def get_friends(self):
		return self.__friends

	def get_opinion(self):
		return self.__opinion

	def push_friend(self, friend):
		self.__friends.append(friend)

class UserDict:
	def __init__(self):
		self.dict = {}

	def push_usr(self, uid):
		if self.dict.has_key(uid):
			return self.dict[uid]
		else:
			self.dict[uid] = Voter(int((random.random() * 3 + 1) / 1) - 2)
			return self.dict[uid]

def parser_main(fname = './facebook/0.edges', directed = False):

	udict = UserDict()
	func = lambda x, y: x.push_friend(y)

	print 'Loading ' + fname + ' file...'
	
	with open(fname, 'r') as fin:
		for line in fin:
			nod_from, nod_to = map(udict.push_usr, map(int,line.strip().split(' ')))
			func(nod_from, nod_to)
			if not directed: func(nod_to, nod_from)

	print 'Edges are successfully loaded!'
	return udict