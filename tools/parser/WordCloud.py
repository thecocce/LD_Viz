from Data import LD_Data,Node

class Word:
	
	def __init__(self,value,sentenceId):
		self._value = value
		self._repetition = 1
		self._sentences = []
		self._sentences.append(sentenceId) 
	
	def addSentence(self,sentenceId):
		# Increment occurence number
		self._repetition+=1
		
		if sentenceId not in self._sentences:
			self._sentences.append(sentenceId)
		#else:
			#print "Sentence " + sentenceId + " already registred for the word " + self._value
	
	def getRepetitionNumber(self):
		#print self._sentences
		return len(self._sentences)

class WordCloud:

	_data = None
	_words = {}
	_done = False
	
	# Word blacklist
	# 't' : negative marker
	# 's' : gerundive marker
	_blacklist = ['a','the','s','t','of','in','to','and','is','on','for']
	
	def __init__(self,ld_data):
		self._data = ld_data
		self._words = {}
		self._done = False
		# start
		for uid,node in self._data.data.iteritems():
			# Extract words from game name
			word_list = self.splitSentence(node._name)
			for word in word_list:
				# Add a new word if needed
				if word in self._words:
					self._words[word].addSentence(uid)
				# If no redundancy, add a new node data
				else:
					self._words[word] = Word(word,uid)
					#print uid + ":" + self.data[uid].name
					
		# end
		self._done = True
		
	
	def splitSentence(self,sentence):
		
		words = []
		tmp_words = sentence
		tmp_words = tmp_words.split(" ")
		
		for tmp in tmp_words:
			tmp = self.wordCleaner(tmp)
			if(tmp != ""):
				words.append(tmp) 
		
		return words
		
	def wordCleaner(self,word):

		result = word.lower()
		# Punctuation
		result = result.replace("'","")
		result = result.replace("-","")
		result = result.replace(".","")
		result = result.replace("!","")
		result = result.replace("?","")
		result = result.replace(":","")
		result = result.replace("&quot","")	# html ';'
		result = result.replace("&amp","") 	# html '&'
		# Word blacklist
		if result in self._blacklist:
			return ""
		
		return result
		
	
	#def generateLinks(self):
		
	#	if self._done:
	#		for w,word in self._words.iteritems():
	#			for word
		
		
		