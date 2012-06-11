import cPickle

class Node:
	
	def __init__(self,uid,name,user,platforms,votes,coolness):
		self._uid = uid
		self._name = self.cleanStr(name)
		self._user = user
		self._platforms = platforms
		self._votes = votes
		self._coolness = coolness
		
	#def __str__(self):
	#	return self.uid
		
	def cleanStr(self,str):
		str = str.replace("'"," ")
		str = str.replace('"'," ")
		str = str.replace("/"," ")
		str = str.replace(";"," ")
		str = str.replace("~"," ")
		return "'"+str+"'"


class LD_Data:
	
	def __init__(self):
		self._data = {}
		
	def addNode(self,uid,name,user,platforms,votes,coolness):
		# Check for data uniqueness
		if uid in self._data:
			print "A node associated with uid " + uid + " is already present in the database."	
		# If no redundancy, add a new node data
		else:
			self._data[uid] = Node(uid,name,user,platforms,votes,coolness)
			#print uid + ":" + self.data[uid].name