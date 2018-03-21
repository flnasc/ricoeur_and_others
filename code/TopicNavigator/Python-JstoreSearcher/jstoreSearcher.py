# Marty Dang 3/17/18

# This program will take user input in the form of a word
# It will then search through the jstore metadata which contains
# xml files and try to match that word to the abstract
# It wiil the output the search results in an HTMl file

import os 
import xml.etree.ElementTree as ET
import re

def findXmlFile(term):

	# Go through directory to reach the xml files 
	# subdir: next directory found
	# dirs: list of subdirectoreis in current dir
	# files: list of files in current dir 
	rootdir = r"/mnt/c/Users/Marty/Documents/GitHub/ricoeur_and_others/code/TopicNavigator/Python-JstoreSearcher/trouble"
	for subdir, dirs, files in os.walk(rootdir):
		for file in files:
			if file.endswith(".xml"):
				item = os.path.join(subdir, file)
				
				# depending on whehter it a book chapter or journal

				if(file.startswith("book")):
					parseBookChapterXmlFile(term, item)
					print("Parsing Book")

				# if(file.startswith("journal")):
				# 	print("Parsing: ", file)
				# 	parseJournalChapterXmlFile(term, item)

# Parse through and find articles that match key word

def parseJournalChapterXmlFile(term, item):

	tree = ET.parse(item)
	root = tree.getroot()
	termFound = False 

	# Stuff I want to find
	attirbutes = ['journal-title', 'publisher-name','article-title',
	'given-names', 'surname', 'day', 'month','year', 'issue-id', 'self-uri'
	,'p','i']

	results = {}

	for item in root.iter():
		for elem in item.iter():

			if(elem.tag in attirbutes):

				# uri is an attirb and also a dictionary
				# need to make it into a usuable link 
				if(elem.tag == "self-uri"):
					dirtyString = str(elem.attrib.values())
					cleanString = dirtyString[14:-3]
					results[elem.tag] = cleanString
					

				# need to extract abstract and combine 
				elif(elem.tag == "p" or elem.tag == "italic"):

					# Some abstracts have text and some have tail
					if(elem.text is not None and elem.tail is not None):
						abstract = elem.text + elem.tail
					elif(elem.text is not None and elem.tail is None):
						abstract = elem.text
					elif(elem.text is None and elem.tail is not None):
						abstract = elem.text
					abstract = str(abstract)
					abstract = abstract.strip()

					# Is term in abstract at all?
					if(term in abstract):
						termFound = True

					results['abstract'] = abstract

				else:
					results[elem.tag] = elem.text

	# No point in storing if term isn't found 
	if(not termFound):
		results.clear()
	else:
		# Now write to HTML File 
		addJournalToHtmlFile(results)

# Parse through and find book chapters that match the term

def parseBookChapterXmlFile(term, item):

	tree = ET.parse(item)
	root = tree.getroot()
	termFoundInBook = False
	termFoundInChapter = False

	# Note there is surname/given name of book and then individual chapters 
	# First line in attribute is for overal book
	# Second line is for individual chapters 
	# Create abstract for book and one for chapter 
	attributes = ['book-title','subtitle','surname','given-names','publisher-name','self-uri',
	'label','title','surname','given-names','p','italic']

	bookInfo = {}

	# First grab the general book's info

	for item in root.iter('book-meta'):
		for elem in item.iter():
			if(elem.tag in attributes):

				# Diff. entry for book authors, subtitles
				if(elem.tag == 'surname'):
					bookInfo['book-surname'] = elem.text

				elif(elem.tag == 'given-names'):
					bookInfo['book-given-names'] = elem.text

				elif(elem.tag == 'subtitle'):
					bookInfo['book-subtitle'] = elem.text

				# self-uri case
				elif(elem.tag == "self-uri"):
					dirtyString = str(elem.attrib.values())
					cleanString = dirtyString[14:-3]
					bookInfo[elem.tag] = cleanString

				# need to extract abstract and combine 
				# this is overal book abstract not individual chapters
				elif(elem.tag == "p" or elem.tag == "italic"):
					# Some abstracts have text and some have tail
					if(elem.text is not None and elem.tail is not None):
						bookAbstract = elem.text + elem.tail
					elif(elem.text is not None and elem.tail is None):
						bookAbstract = elem.text
					elif(elem.text is None and elem.tail is not None):
						bookAbstract = elem.text
					bookAbstract = str(bookAbstract)
					bookAbstract = bookAbstract.strip()

					# Is term in abstract at all?
					if(term in bookAbstract):
						termFoundInBook = True

					bookInfo['book-abstract'] = bookAbstract

				else:
				    # All other cases 
				    bookInfo[elem.tag] = elem.text

	# Next grab individual chapters

	for item in root.iter('book-part-meta'):
		for elem in item.iter():
		    if(elem.tag in attributes):

		    	# chapter authors 

		        if(elem.tag == 'surname'):
		            bookInfo['chapter-surname'] = elem.text

		        elif(elem.tag == 'given-names'):
		            bookInfo['chapter-give-names'] = elem.text	

		        elif(elem.tag == 'subtitle'):
		        	bookInfo['chapter-subtitle'] = elem.text

		        # need to extract abstract and combine 
				# this is overal book abstract not individual chapters    
		        elif(elem.tag == "p" or elem.tag == "italic"):

		        	# Some abstracts have text and some have tail
		        	if(elem.text is not None and elem.tail is not None):
		        		chapterAbstract = elem.text + elem.tail

		        	elif(elem.text is not None and elem.tail is None):
		        		chapterAbstract = elem.text

		        	elif(elem.text is None and elem.tail is not None):
		        		chapterAbstract = elem.text

		        	chapterAbstract = str(chapterAbstract)
		        	chapterAbstract = chapterAbstract.strip()

		        	if(term in chapterAbstract):
		        		termFoundInChapter = True

		        	bookInfo['chapter-abstract'] = chapterAbstract

		        else:
		        	bookInfo[elem.tag] = elem.text
		if(not termFoundInChapter and not termFoundInBook):
		    bookInfo.clear()
		else:
		    addBooktoHtmlFile(bookInfo)

		
# will create an html file with the results 
def createHtmlFile():

	f = open('Digital Ricoeur-JStor Navigator.html','w') #create another file
	f.write('<!-- File generated by Marty Dang-->' + '\n')

	#Add in the standard HTMl stuff
	# <!DOCTYPE html> 
    # <html lang="en">
    # <body> 
	f.write('<!DOCTYPE html>' + '\n')
	f.write('<html lang=' + '"en"'+ '>' + '\n')
	f.write('<meta charset="utf-8">' + '\n' + '\n')
	f.write('  ' + '<body>' + '\n')
	f.write( '  ' + '<center><h2>Digital Ricoeur - Jstor Navigator</h2></center>' + '\n' +'\n')
	f.write('  ' + '<p>' + '\n')
	# f.write('  ' + '</body>' + '\n')
	# f.write('</html>')

	print("File creation complete")

def addBooktoHtmlFile(dictionaryOfResults):
    f = open('Digital Ricoeur-JStor Navigator.html','a') # open up the file
    if("book-title" in dictionaryOfResults.keys()):
    	f.write("    " + "Book Title: " + dictionaryOfResults["book-title"] + "-")

    if("book-subtitle" in dictionaryOfResults.keys()):
    	f.write(dictionaryOfResults["book-subtitle"] + '<br>' + '\n')

    if("publisher-name" in dictionaryOfResults.keys()):
    	f.write("    " + "Publisher: " + dictionaryOfResults["publisher-name"] + '<br>' + '\n')

    if("book-surname" in dictionaryOfResults.keys()):
    	f.write("    " + "Author(s): " + dictionaryOfResults['book-surname'])

    if("book-given-names" in dictionaryOfResults.keys()):
    	f.write(" " + dictionaryOfResults["book-given-names"] + '<br>' + '\n')

    if("label" in dictionaryOfResults.keys()):
    	f.write("        " + dictionaryOfResults["label"] + '<br>' + '\n')



    f.write("    " + "Link: " + '<a href=' + '"' + dictionaryOfResults["self-uri"] + '"'+ 
    	'>'+ dictionaryOfResults["self-uri"]  + '</a>' + ' '+ '<br>' + '\n' + '\n')

def addJournalToHtmlFile(dictionaryOfResults):
    f = open('Digital Ricoeur-JStor Navigator.html','a') # open up the file
    f.write("    " + "Journal Title: " + dictionaryOfResults["journal-title"] + '<br>' +'\n')
    f.write("    " + "Publisher: " + dictionaryOfResults["publisher-name"] + '<br>' + '\n')
    f.write("    " + "Issue: " + dictionaryOfResults["issue-id"] + '<br>' + '\n')

    if("month" in dictionaryOfResults.keys()):
    	f.write("    " + "Date: " + dictionaryOfResults["month"] + " ")

    if("day" in dictionaryOfResults.keys()):
    	f.write(dictionaryOfResults["day"] + ", ")

    if("year" in dictionaryOfResults.keys()):
    	f.write(dictionaryOfResults["year"] + '<br>' + '\n')

    if("surname" in dictionaryOfResults.keys()):
    	f.write("    " + "Author(s): " + dictionaryOfResults["surname"])

    if("given-names" in dictionaryOfResults.keys()):
    	f.write(" " + dictionaryOfResults["given-names"] + '<br>' + '\n')

    f.write("    " + "Abstract: " + dictionaryOfResults["abstract"] + '<br>' + '\n')
    f.write("    " + "Link: " + '<a href=' + '"' + dictionaryOfResults["self-uri"] + '"'+ 
    	'>'+ dictionaryOfResults["self-uri"]  + '</a>' + ' '+ '<br>' + '\n' + '\n')

   
# Allow the user to enter in multiple words seperaeted by
# comma to generate multiple at once 
def main():

	# create the initial HTML File
	createHtmlFile()
	term = input("Please enter in your word: ")
	findXmlFile(term)

if __name__ == "__main__": main()