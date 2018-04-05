# Marty Dang 3/17/18

# This program will take user input in the form of a word
# It will then search through the jstore metadata which contains
# xml files and try to match that word to the abstract
# It wiil the output the search results in an HTMl file

import os 
import time
import xml.etree.ElementTree as ET

globalBook = 0
globalJournal = 0
globalOpen = 0

def incrementBook():
	global globalBook
	globalBook += 1

def incrementJournal():
	global globalJournal
	globalJournal += 1

def clearCounters():
	global globalBook
	global globalJournal
	globalBook = 0 
	globalJournal = 0 

def incrementOpen():
	global globalOpen
	globalOpen +=1


# Takes a list of terms
# Finds location of xml files 
# Calls the parse functions for book and chapter
def findXmlFile(term): 

	# Need to clear counters for serach results from prev search 
	clearCounters()

	# Go through directory to reach the xml files 
	# subdir: next directory found
	# dirs: list of subdirectoreis in current dir
	# files: list of files in current dir 

	# Change this line for location of files
	rootdir = r"/mnt/c/Users/Marty/Documents/GitHub/ricoeur_and_others/code/TopicNavigator/Python-JstoreSearcher/jstor_metadata"

	start1 = time.time()

	for subdir, dirs, files in os.walk(rootdir):
		for file in files:
			if file.endswith(".xml"):
				item = os.path.join(subdir, file)
				
				# depending on whehter it a book chapter or journal
				if(file.startswith("book")):
					parseBookChapterXmlFile(term, item, file)
					print("Parsed ", file, " for: ", term)

				if(file.startswith("journal")):
					parseJournalChapterXmlFile(term, item, file)
					print("Parsed", file, " for: ", term)
	end1 = time.time()
	print("Time it took to complete search for word: ", str(term), str(end1-start1))


# Parse through and find articles that match key word
def parseJournalChapterXmlFile(term, item, file):

	# Using Element Tree
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
					

				# abstracts are a bit tricky to deal with
				# Print out parts to see why. The number
				# changes alot
				elif(elem.tag == "p"):

					parts = list(elem.iter())
					counter = 0
					abstract = ""

					while(counter != len(parts)):
						abstract = abstract + str(parts[counter].text) + str(parts[counter].tail)
						counter += 1

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
		incrementJournal()
		addJournalToHtmlFile(results, file, term)
		termFound = False

# Parse through and find book chapters that match the term
def parseBookChapterXmlFile(term, item, file):

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
	chapterInfo = {}

	# First grab the general book's info
	for item in root.iter('book-meta'):
		for elem in item.iter():
			if(elem.tag in attributes):	
				if(elem.tag == 'surname'):
					bookInfo['book-surname'] = elem.text
				elif(elem.tag == 'given-names'):
					bookInfo['book-given-names'] = elem.text
				elif(elem.tag == 'subtitle'):
					bookInfo['book-subtitle'] = elem.text
				# again uri is kind of dirty 
				elif(elem.tag == "self-uri"):
					dirtyString = str(elem.attrib.values())
					cleanString = dirtyString[14:-3]
					bookInfo[elem.tag] = cleanString

				elif(elem.tag == "p"):
					parts = list(elem.iter())
					counter = 0
					bookAbstract = ""

					while(counter != len(parts)):
						bookAbstract = bookAbstract + parts[counter].text + parts[counter].tail
						counter += 1

					bookAbstract = bookAbstract.strip()

					if(term in bookAbstract):
						termFoundInBook = True
						bookInfo['book-abstract'] = bookAbstract
				else:
					bookInfo[elem.tag] = elem.text

	if(termFoundInBook):
		incrementBook()
		addBooktoHtmlFile(bookInfo, file, term)

    # Next grab info of individual chapters
	for item in root.iter('book-part-meta'):
		for elem in item.iter():
			if(elem.tag in attributes):

				if(elem.tag == 'surname'):
					chapterInfo['chapter-surname'] = elem.text

				elif(elem.tag == 'given-names'):
					chapterInfo['chapter-given-names'] = elem.text	

				elif(elem.tag == 'subtitle'):
					chapterInfo['chapter-subtitle'] = elem.text

				elif(elem.tag == "p"):

					parts = list(elem.iter())
					counter = 0
					chapterAbstract = ""

					while(counter != len(parts)):
						chapterAbstract = chapterAbstract + parts[counter].text + parts[counter].tail
						counter += 1

					chapterAbstract = chapterAbstract.strip()

					if(term in chapterAbstract):
						
						termFoundInChapter = True
						chapterInfo['chapter-abstract'] = chapterAbstract
				else:
					chapterInfo[elem.tag] = elem.text

		if(not termFoundInChapter):
			chapterInfo.clear()
		else:
			incrementBook()
			addChaptertoHtmlFile(chapterInfo,bookInfo, file, term)
			chapterInfo.clear()
			termFoundInChapter = False


# create html files for the amount of items in term list
def createHtmlFiles(term):

	f = open('Digital-Ricoeur-JStor-'+ term +'.html', 'w')
	f.write('<!-- File generated by Marty Dang-->' + '\n')

	#Add in standard HTML stuff

	f.write('<!DOCTYPE html>' + '\n')
	f.write('<html lang=' + '"en"'+ '>' + '\n')
	f.write('<meta charset="utf-8">' + '\n' + '\n')
	f.write('  ' + '<body>' + '\n')
	f.write('  ' + '<center><h2>Digital Ricoeur - JStor </h2></center>' + '\n' +'\n')
	f.write('  ' + '<h3>Search Term: ' + term + '</h3')
	f.write('  ' + '<h3>Number of Book Results: ### ' + '</h3')
	f.write('  ' + '<h3>Number of Journal Results: !!! ' + '</h3' + '<br>')
	f.write('  ' + '<p>' + '\n')

	f.close()

def addBooktoHtmlFile(dictionaryOfResults, file, term):
    f = open('Digital-Ricoeur-JStor-'+ term +'.html','a') # open up the file
    incrementOpen()
    f.write('<br>' + '\n')
    f.write("File: " + file + '\n')
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

    f.write("    Abstract: " + dictionaryOfResults["book-abstract"] + '<br>' + '\n')

    f.write("    " + "Link: " + '<a href=' + '"' + dictionaryOfResults["self-uri"] + '"'+ 
    	'>'+ dictionaryOfResults["self-uri"]  + '</a>' + ' '+ '<br> ' + '<br>' + '\n' + '\n')

    f.close()

def addChaptertoHtmlFile(chapterInfo, bookInfo, file, term):
    f = open('Digital-Ricoeur-JStor-'+ term +'.html','a') # open up the file 
    incrementOpen()
    f.write("File: " + file + '\n')

    if("label" in chapterInfo.keys()):
    	f.write("  " + chapterInfo["label"])

    if("title" in chapterInfo.keys()):
    	f.write("  " + chapterInfo["title"])

    if("book-title" in bookInfo.keys()):
    	f.write(" from: " + '<a href=' + '"' + bookInfo["self-uri"] + '"' + '>' + bookInfo["book-title"] + '</a>' + '<br>' + '\n' )
    else:
    	f.write('<br>' + '\n')

    if("chapter-surname" in chapterInfo.keys()):
    	f.write("Author(s) " + chapterInfo["chapter-surname"])

    if("chapter-given-names" in chapterInfo.keys()):
    	f.write(" " + chapterInfo["chapter-given-names"] + '<br>' + '\n')

    if('chapter-abstract' in chapterInfo.keys()):
    	f.write(" " + "Abstract: " + chapterInfo['chapter-abstract'] + '<br>' + '<br>'+ '\n' + '\n' + '\n')

    f.close()


def addJournalToHtmlFile(dictionaryOfResults, file, term):
    f = open('Digital-Ricoeur-JStor-'+ term +'.html','a') # open up the file
    incrementOpen()
    f.write("File: " + file + '\n')

    if("journal-title" in dictionaryOfResults.keys()):
    	f.write("    " + "Journal Title: " + dictionaryOfResults["journal-title"] + '<br>' +'\n')

    if("publisher-name" in dictionaryOfResults.keys()):
    	f.write("    " + "Publisher: " + dictionaryOfResults["publisher-name"] + '<br>' + '\n')

    if("issue-id" in dictionaryOfResults.keys()):
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
    	'>'+ dictionaryOfResults["self-uri"]  + '</a>' + ' '+ '<br>' + '<br>'+ '\n' + '\n')

    f.close()

# iterate through and find place holders and replace with counters
def writeCounters(term):
	with open('Digital-Ricoeur-JStor-'+ term +'.html','r') as f:
		data = f.readlines()
		data[8] = data[8].replace('###',str(globalBook))
		data[8] = data[8].replace('!!!',str(globalJournal))

	with open('Digital-Ricoeur-JStor-'+ term +'.html', 'w') as f:
		f.writelines(data)

# Allow the user to enter in multiple words seperaeted by
# comma to generate multiple at once 
def main():

	# Change the stuff here to search for terms
	terms = ['history']

	for term in terms:

		start = time.time()

		createHtmlFiles(term)
		findXmlFile(term)
		writeCounters(term)

		f = open('Digital-Ricoeur-JStor-'+ term +'.html','a')
		f.write('  ' + '</body>' + '\n')
		f.write('</html>')
		f.close()

		end = time.time()

	print("Overall Time for 6 words: ", str(end-start) + " sec ")
	print("Time files were open: ", globalOpen)

if __name__ == "__main__": main()