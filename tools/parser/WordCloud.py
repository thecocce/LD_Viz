from Data import LD_Data,Node

class Word:
	
	def __init__(self,value,sentenceId):
		self._value = value
		self._repetition = 1
		self._sentences = []
		self._sentences.append(sentenceId) 
	
	def __str__(self):
		return self._value
	
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

class Sentence:
	
	def __init__(self,value,sentenceId):
		self._value = value
		self._sentenceId = sentenceId
		self._words = []
		
	def addWord(self,word):
		if word not in self._words:
			self._words.append(word)

class WordCloud:

	_data = None
	_words = {}		# Link word -> sentences
	_sentences = {}	# Link sentence -> words
	_links = 0
	_done = False
	
	# Word blacklist
	# 't' : negative marker
	# 's' : gerundive marker
	_blacklist = ['a','the','s','t','of','in','to','and','is','on','for']
	
	def __init__(self,ld_data):
		self._data = ld_data
		self._words = {}
		self._sentences = {}
		self._done = False
		# start
		for uid,node in self._data._data.iteritems():
			# Create sentence node
			sentence = node._name
			self._sentences[uid] = Sentence(sentence,uid)
			# Extract words from game name
			word_list = self.splitSentence(sentence)
			for word in word_list:
				# Add a new word if needed
				if word in self._words:
					self._words[word].addSentence(uid)
				# If no redundancy, add a new node data
				else:
					self._words[word] = Word(word,uid)
					#print uid + ":" + self.data[uid].name
				# Also link current sentence to its words
				self._sentences[uid].addWord(word)	
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
		result = result.replace("(","")
		result = result.replace(")","")
		result = result.replace("&quot","")	# html ';'
		result = result.replace("&amp","") 	# html '&'
		# Word blacklist
		if result in self._blacklist:
			return ""
		
		return result
	
	# Print miscellaneous piece of information
	def printStats(self):
		print "WordCloud stats:"
		print "- sentence count: " + str(len(self._sentences))
		print "- word count: " + str(len(self._words)) 
		print "- word blacklist: " + str(self._blacklist)
		print "- links number:" + str(self._links)
	
		
	# Output data concerning words linked together.
	# . For instance, let's consider 'A','AB','CBD' as three sentences...
	# . composed with the respective letters a,b,c and d
	# . 'AB' -> [a,b] | 'ABC' -> [a,b,c] | 'CBD' -> [c,b,d]
	# . then we have the following links:
	# . For the word a: a -> b
	# . For the word b: b -> a | b -> c | b -> d
	# . For the word c: c -> b | c -> d
	# . And for the word d: d -> b | d -> c
 	def generateWordCorrelations(self):
		
		data = {}
		self._links = 0
		
		# Need a generated WordCloud
		if not self._done:
			return
		
		# O(2^n) exploration algorithm
		# Could be certainly optimized but worst cases seldom if never occur
		for w,word_base in self._words.iteritems():
			data[word_base] = []
			for sentenceId in word_base._sentences:
				for word in self._sentences[sentenceId]._words:
					if word not in data[word_base] and word != str(word_base):
						data[word_base].append(word)
						self._links+=1
						
			print "{'"+str(word_base) + "':" + str(data[word_base]) + "},\n"	 
		
		
		return data
		