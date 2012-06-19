from Data import LD_Data,Node

class Game:
	
	def __init__(self,gameId,name):
		self._name = name
		self._gameId = gameId
		self._platforms = []
		
	def addPlatform(self,platform):
		if platform == None:
			return
		# Single platform
		if isinstance(platform, basestring) and platform not in self._platforms:
			self._platforms.append(platform)
		# Multiple platform
		else:
			for p in platform:
				if p not in self._platforms:
					self._platforms.append(platform) 
		
	def __str__(self):
		return self._name

class MultiPlatform:

	_data = None
	_games = {}		# Link word -> sentences
	_totalGames = 0
	_platforms = {'windows':0,'osx':0,'linux':0,'web':0,'android':0,'ios':0}
	_subPlatforms = {'unity':['windows','osx'],
					 'mac':['osx'],
					 'java':['windows','osx','linux'],
					 'jar':['windows','osx','linux'],
					 'flash':['web'],
					 'swf':['web'],
					 'html':['web'],
					 'xna':['windows'],
					} 
	_done = False
	
	def __init__(self,ld_data):
		# Reset internal data
		self._data = ld_data
		self._games = {}
		self._totalGames = 0
		for p in self._platforms:
			self._platforms[p] = 0
			
		# For each game, we extract its platform(s)
		for uid,game in self._data._data.iteritems():
			# Create game node
			name = self.wordCleaner(game._name)
			self._games[uid] = Game(uid,name)
			self._totalGames+=1
			# Extract platforms
			for platform_temp in game._platforms:
				platform = self.platformAnalysis(platform_temp)
				if platform != None:
					self._games[uid].addPlatform(platform)
					self._platforms[platform]+=1
				# Debug: See what's wrong with this platform
				#else:
				#	print platform_temp
			# Remove games with no platform recognized
			if self._games[uid]._platforms == []:
				del self._games[uid]
			
		# end
		self._done = True


	def platformAnalysis(self,value):
		platform = self.wordCleaner(value,True)
		# first level
		for p in self._platforms:
			if platform.find(p) != -1:
				return p
		# second level
		for sp in self._subPlatforms:
			if platform.find(sp) != -1:
				return p
		return None
	
	def wordCleaner(self,word,hard=False):

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
		result = result.replace("/","")
		result = result.replace("\\","")
		result = result.replace(";","")
		result = result.replace("&","")
		result = result.replace("`","")
		result = result.replace("&quot","")	# html ';'
		result = result.replace("&amp","") 	# html '&'
		if hard:
			result = result.replace(" ","")
		return result


	# Print miscellaneous piece of information
	def printStats(self):
		print "MultiPlatform stats:"
		print "- platforms: " + str(self._platforms) 
		ag = len(self._games)
		tg = self._totalGames
		upg = tg - ag
		print "- game count: " + str(ag) + "/" + str(tg) + " ~ "+ str(upg) +" with unknown platform " + "("+str(float(100*upg)/float(tg))+" %)"

