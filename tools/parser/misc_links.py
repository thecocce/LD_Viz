##
# LD_Viz ~ cboissie 2012
##
# About: This is a dirty script for extracting data from misc_links HTML, and convert it to a JSON formalism
# NB: Please README.md for more information concerning the misc_links parsing.

import sys
import re
from Data import LD_Data,Node
from WordCloud import WordCloud

def start(file):
	file = open(file,'r')
	#json = "{games:[\n"
	ld_data = LD_Data()
	content = file.read()
	
	# List all entries
	entries = content.split("<tr>")
	entries.pop(0) # Remove first empty line
	
	# Catch data from each entry
	# uid, name, user, platform_list, votes, coolness
	for entry in entries:	
		# Parse internal entry data
		data = entry.split("<td>")
		# Extract each values
		rg = re.compile('.*?(\\d+)',re.IGNORECASE|re.DOTALL)
		uid = rg.search(data[1]).group(1)
		name = re.search("(?<=>)[^<]+?(?=<)",data[1]).group(0) 
		user = data[2]
		platform_list = []
		for platform_link in data[3].split("|"):
			platform = re.search("(?<=>)[^<]+?(?=<)",platform_link)
			if platform:
				platform_list.append(platform.group(0))
		votes = data[4]
		coolness = data[5]
		
		ld_data.addNode(uid,name,user,platform_list,votes,coolness)
		# Create the JSON string
		#json+="{'uid':"+uid+",'name':"+cleanStr(name)+",'user':"+cleanStr(user)+",'plaforms':["
		#for platform in platform_list:
		#	json+=cleanStr(platform)+","
		#json+="],'votes':"+votes+",'coolness':"+coolness+"},\n"
		
	#json += "]}"
	#print json
	test = WordCloud(ld_data)
	for word,d in test._words.iteritems():
		if(d.getRepetitionNumber()>1):
			print word + " x " + str(d.getRepetitionNumber())# + ", linked to " + str(d._sentences)
	
	
	
# Just type ">misc_links.py path/to/data.htm"
if __name__ == '__main__':

	if len(sys.argv) != 2:
		print "Please specify a file in the command line."
		# Default data (for testing purpose)
		# file = "data/html/ld22_misc_links.htm"
	else:
		file = sys.argv[1]
		start(file)