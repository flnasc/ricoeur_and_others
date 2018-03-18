# Marty Dang 3/17/18

# This program will take user input in the form of a word
# It will then search through the jstore metadata which contains
# xml files and try to match that word to the abstract
# It wiil the output the search results in an HTMl file

import os 
import xml.etree.ElementTree as ET

def findXmlFile(term):

	# Go through directory to reach the xml files 
	# subdir: next directory found
	# dirs: list of subdirectoreis in current dir
	# files: list of files in current dir 
	rootdir = r"/mnt/c/Users/Marty/Documents/GitHub/ricoeur_and_others/code/TopicNavigator/Python-JstoreSearcher"
	for subdir, dirs, files in os.walk(rootdir):
		for file in files:
			if file.endswith(".xml"):
				item = os.path.join(subdir, file)
				# print(file)
				parseXmlFile(term, item)

# Parse through and find articles that match key word
def parseXmlFile(term, item):

	tree = ET.parse(item)
	root = tree.getroot()

	# for event, elem in ET.iterparse(item, events=('start','end')):
	# 	if event == 'start':
	# 		print(elem.tag)
	# 	elif event == 'end':
	# 		if elem.text is not None and elem.tail is not None:
	# 			print(repr(elem.tail))


	for item in root.iter('abstract'):
		for thing in item.iter():
			abstract = thing.text + thing.tail
			if(term in abstract.strip()):
				print("True")
			else:
				print("False")
			# print(''.join(root.itertext()))





		
# will create an html file with the results 
def createHtmlFile():
	print("File creation complete")

def addToHtmlFile():
	print("Adding complete")

# Allow the user to enter in multiple words seperaeted by
# comma to generate multiple at once 
def main():

	# create the initial HTML File
	createHtmlFile()
	term = input("Please enter in your word: ")
	findXmlFile(term)

if __name__ == "__main__": main()