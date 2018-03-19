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
				
				# Depending on whehter it a book chapter or journal
				if(file.startswith("book")):
					parseBookChapterXmlFile(term, item)
					print("Parsing Book")

				if(file.startswith("journal")):
					parseJournalChapterXmlFile(term, item)
					print("Parsing Journal")

# Parse through and find articles that match key word

def parseJournalChapterXmlFile(term, item):
	print("Parsing")

def parseBookChapterXmlFile(term, item):

	tree = ET.parse(item)
	root = tree.getroot()
	
	# for child in root:
	# 	print("2nd Level: ", child.tag)
	# 	for granchild in child:
	# 		print("    3rd Level: ", granchild.tag)
	# 		for supergranchild in granchild:
	# 			print("        4th Level: ", supergranchild.tag)
	# 			for supersupergranchild in supergranchild:
	# 				print("            5th Level: ", supersupergranchild.tag)
	# 				for ultragranchild in supersupergranchild:
	# 					print("                6th Level: ", ultragranchild.tag)
	# 					for wowgranchild in ultragranchild:
	# 						print("                    7th Level: ", wowgranchild.tag)
	# 						for wowowgranchild in wowgranchild:
	# 							print("                        8th Level: ", wowowgranchild.tag)
	# 							for nochild in wowowgranchild:
	# 								print("                            9th Level: ", nochild.tag)
	# 								for fuck in nochild:
	# 									print("                              10th Level: ", fuck.tag)


	relevantStuff = ['label','title', 'subtitle','surname', 'given-names','p','italic']
	relevant = {}

	for item in root.iter('book-part-meta'):
		for elem in item.iter():

			if(elem.tag in relevantStuff):

				relevant[elem.tag] = elem.text

				if(elem.tag == "p" or elem.tag == "italic"):
					abstract = elem.text + elem.tail
					abstract = abstract.strip()
					relevant['abstract'] = abstract

					if(term in abstract):
						if('p' in relevant.keys()):
							del relevant['p']
						if('italic' in relevant.keys()):
							del relevant['italic']
						print(relevant, "\n")				

    # Then grab book title, publisher name, link and authors

	stuffWeWant = ["book-title", "subtitle", "surname", "given-names", "publisher-name","self-uri"]
	bookInfo = {}

	for item in root.iter('book-meta'):
		for elem in item.iter():
			if(elem.tag in stuffWeWant):
				bookInfo[elem.tag] = elem.text
				if(elem.tag == "self-uri"):
					bookInfo[elem.tag] = elem.attrib



		
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