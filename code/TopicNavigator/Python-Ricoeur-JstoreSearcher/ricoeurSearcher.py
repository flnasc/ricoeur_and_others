# Marty Dang 5/24/18
# This program is another version of jstoresearcher but will
# minimize the amt of times the file is open in order to 
# speed things up

import os
import time
import xml.etree.ElementTree as ET
import io
import re

# Keeps track of amt. for search results
globalBook = 0
globalJournal = 0

# increments the counter keeping track of the amt. of book results
def incrementBook():
	global globalBook
	globalBook += 1

# increments the counter keeping track of the amt. of journal results. 
def incrementJournal():
	global globalJournal
	globalJournal += 1

# Set both the book and journal counter to 0 
def clearCounters():
	global globalBook
	global globalJournal
	globalBook = 0 
	globalJournal = 0 
	

# create html files for the amount of items in term list
# takes in the term we are searching for and f, which is the html file we are writing to. 
def createHtmlFiles(term,f):

	f.write('<!-- File generated by Marty Dang-->' + '\n')

	#Add in standard HTML stuff
	f.write('<!DOCTYPE html>' + '\n')
	f.write('<html lang=' + '"en"'+ '>' + '\n')
	f.write('<meta charset="utf-8">' + '\n' + '\n')
	f.write('  ' + '<body>' + '\n')
	f.write('  ' + '<center><h2>Digital Ricoeur - JStor </h2></center>' + '\n' +'\n')
	f.write('  ' + '<h3>Ricoeur appearing with '+'Search Term: ' + term + '</h3>' + '\n')
	f.write('  ' + '<h3>Book Results: ### ' + '</h3>' + '\n')
	f.write('  ' + '<h3>Journal Results: !!! ' + '</h3>' + '<br>' + '\n')
	f.write('  ' + '<p>' + '\n')

# Takes a list of terms
# Finds location of xml files 
# Calls the parse functions for book and chapter
def findXmlFile(term,f): 		

	# Need to clear counters for serach results from prev search 
	clearCounters()

	# Go through directory to reach the xml files 
	# dirname: the next directory
	# subdirList: A list of sub-directories in current directory
	# files a list of files in the current directory

	# Change this line for location of files
	rootdir = "../../.."

	for dirName, subdirList, files in os.walk(rootdir):
		# print('Found directory: %s' % dirName)
		if(dirName == "../../../data/jstor_metadata-Clean"):

			for file in files:
				if file.endswith(".xml"):
					item = os.path.join(dirName, file)

					#depending on whehter it a book chapter or journal
					if(file.startswith("book")):
						parseBookChapterXmlFile(term, item, file, f)
						#print(file)

					if(file.startswith("journal")):
						parseJournalChapterXmlFile(term, item, file, f)	
						#print(file)					

# Parse through and find articles that match key word
def parseJournalChapterXmlFile(term, item, file,f):

	# Using Element Tree
	tree = ET.parse(item)
	root = tree.getroot()
	termFound = False 
	ricoeurFound = False

	# Stuff I want to find
	attirbutes = ['journal-title', 'publisher-name','article-title',
	'given-names', 'surname', 'day', 'month','year', 'issue-id', 'self-uri'
	,'p','i']

	# Once I find the stuff I want, I will put it in a dictionary called results. 
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
				    
				    # Regex expression to just find our term. We used this instead of dictionary
				    # look up for stricter results. 
					searchObj = re.search('\W'+term+'\W', abstract, re.IGNORECASE)

					if(searchObj):
						termFound = True
						results['abstract'] = abstract

				else:
					results[elem.tag] = elem.text
	# Also check to see if Ricoeur is found
	for key, value in results.items():
		if(key is not None and value is not None):
			if("Ricoeur" in value):
				ricoeurFound = True

	if(ricoeurFound and termFound):
		incrementJournal()
		addJournalToHtmlFile(results, file, term,f)

	results.clear()
	termFound = False
	ricoeurFound = False

# Parse through and find book chapters that match the term
def parseBookChapterXmlFile(term, item, file,f):

	tree = ET.parse(item)
	root = tree.getroot()
	termFoundInBook = False
	termFoundInChapter = False
	ricoeurFound = False

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

				elif(elem.tag == 'book-title'):
					bookInfo[elem.tag] = elem.text

				elif(elem.tag == "p"):
					parts = list(elem.iter())
					counter = 0
					bookAbstract = ""

					while(counter != len(parts)):
						bookAbstract = bookAbstract + parts[counter].text + parts[counter].tail
						counter += 1

					bookAbstract = bookAbstract.strip()
					# regex expression 
					searchObj = re.search('\W'+term+'\W', bookAbstract, re.IGNORECASE)

					if(searchObj):
						termFoundInBook = True
						bookInfo['book-abstract'] = bookAbstract

				else:
					bookInfo[elem.tag] = elem.text
	# Checking to be sure term and Ricoeur are both found
	for key, value in bookInfo.items():
		if(key is not None and value is not None):
			if("Ricoeur" in value):
				ricoeurFound = True


	if(termFoundInBook and ricoeurFound):
		incrementBook()
		addBooktoHtmlFile(bookInfo, file, term,f)
		ricoeurFound = False
	else:
		ricoeurFound = False
		termFoundInBook = False


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
					# regex expression 
					searchObj = re.search('\W'+term+'\W', chapterAbstract, re.IGNORECASE)

					if(searchObj):
						termFoundInChapter = True
						chapterInfo['chapter-abstract'] = chapterAbstract
						
				else:
					chapterInfo[elem.tag] = elem.text 
    # Check to be sure both Ricoeur and term are found
	for key, value in chapterInfo.items():
		if(key is not None and value is not None):
			if("Ricoeur" in value):
				ricoeurFound = True


	if(not termFoundInChapter or not ricoeurFound):
		chapterInfo.clear()
	else:
		incrementBook()
		addChaptertoHtmlFile(chapterInfo,bookInfo, file, term,f)

	bookInfo.clear()
	chapterInfo.clear()
	termFoundInChapter = False
	ricoeurFound = False

# Writes contents into HTML File
# This is for the parts of a book
# Takes in the dictionary which has the results, the file (for debug purposes),
# the serach term, and the then file you are writing to. 
def addBooktoHtmlFile(dictionaryOfResults, file, term, f):

    if("book-title" in dictionaryOfResults.keys()):
    	f.write("  " + "Book Title: " + dictionaryOfResults["book-title"] + "-")

    if("book-subtitle" in dictionaryOfResults.keys()):
    	f.write(dictionaryOfResults["book-subtitle"] + '<br>' + '\n')

    if("publisher-name" in dictionaryOfResults.keys()):
    	f.write("  " + "Publisher: " + dictionaryOfResults["publisher-name"] + '<br>' + '\n')

    if("book-surname" in dictionaryOfResults.keys()):
    	f.write("  " + "Author(s): " + dictionaryOfResults['book-surname'])

    if("book-given-names" in dictionaryOfResults.keys()):
    	f.write(" " + dictionaryOfResults["book-given-names"] + '<br>' + '\n')

    if(len(dictionaryOfResults['book-abstract']) > 2000):
    		dictionaryOfResults['book-abstract'] = dictionaryOfResults['book-abstract'][:2000]	
    		f.write("  Abstract: " + dictionaryOfResults["book-abstract"] + "~"+ '<br>' + '\n')
    else:
    	f.write("  Abstract: " + dictionaryOfResults["book-abstract"] + '<br>' + '\n')

    f.write("  " + "Link: " + '<a href=' + '"' + dictionaryOfResults["self-uri"] + '"'+ ' target="_blank" ' +
    	'>'+ dictionaryOfResults["self-uri"]  + '</a>' + ' '+ '<br> ' + '\n')

    f.write(file)

    f.write("  <hr>" + '<br>' + '\n' + '\n' )

# Writes contents into HTML File
# This is for the chapter in the book 
# Takes in the dictionary which has the results, the file (for debug purposes),
# the serach term, and the then file you are writing to. 
def addChaptertoHtmlFile(chapterInfo, bookInfo, file, term,f):

    if("label" in chapterInfo.keys()):
    	f.write("  " + chapterInfo["label"])

    if("title" in chapterInfo.keys()):
    	f.write("  " + chapterInfo["title"] + '<br>' + '\n')

    if("chapter-subtitle" in chapterInfo.keys()):
    	f.write("  " + chapterInfo["chapter-subtitle"])

    if("book-title" in bookInfo.keys()):
    	f.write(" from: " + '\n'+'  <a href=' + '"' + bookInfo["self-uri"] 
    		+ '"'  +'>' + bookInfo["book-title"] + '</a>' + '<br>' + '\n' )
    else:
    	f.write('<br>' + '\n')

    if("chapter-surname" in chapterInfo.keys()):
    	f.write("  Author(s) " + chapterInfo["chapter-surname"])

    if("chapter-given-names" in chapterInfo.keys()):
    	f.write(" " + chapterInfo["chapter-given-names"] + '<br>' + '\n')

    if('chapter-abstract' in chapterInfo.keys()):
    	if(len(chapterInfo['chapter-abstract']) > 2000):
    		chapterInfo['chapter-abstract'] = chapterInfo['chapter-abstract'][:2000]
    		f.write("  Abstract: " + chapterInfo['chapter-abstract'] + "~"+ '<br>' + '\n')
    	else:
    		f.write("  Abstract: " + chapterInfo['chapter-abstract'] + '<br>' + '\n')

    if("self-uri" in chapterInfo.keys()):
    	f.write("  " + "Link: " + '<a href=' + '"' + bookInfo["self-uri"] + '"'+ + ' target="_blank" ' + '>'+ bookInfo["self-uri"]  + '</a>' + ' '+ '<br> ' + '\n')
    f.write(file)


    f.write("  <hr>" + '<br>' + '\n' + '\n' )

# Writes contents into HTML File
# This is for the journals 
# Takes in the dictionary which has the results, the file (for debug purposes),
# the serach term, and the then file you are writing to. 
def addJournalToHtmlFile(dictionaryOfResults, file, term,f):

    if("journal-title" in dictionaryOfResults.keys()):
    	f.write("Journal Title: " + dictionaryOfResults["journal-title"] 
    		+ '<br>' +'\n')

    if("article-title" in dictionaryOfResults.keys() and dictionaryOfResults["article-title"] != None):
    	f.write("Article Title: " + dictionaryOfResults["article-title"]
    		+ '<br>' + '\n')

    if("publisher-name" in dictionaryOfResults.keys()):
    	f.write("Publisher: " + dictionaryOfResults["publisher-name"] 
    		+ '<br>' + '\n')

    if("issue-id" in dictionaryOfResults.keys()):
    	f.write("Issue: " + dictionaryOfResults["issue-id"] 
    		+ '<br>' + '\n')

    if("month" in dictionaryOfResults.keys()):
    	f.write("Date: " + dictionaryOfResults["month"] + " ")

    if("day" in dictionaryOfResults.keys()):
    	f.write(dictionaryOfResults["day"] + ", ")

    if("year" in dictionaryOfResults.keys()):
    	f.write(dictionaryOfResults["year"] + '<br>' + '\n')

    if("surname" in dictionaryOfResults.keys()):
    	f.write("Author(s): " + dictionaryOfResults["surname"])

    if("given-names" in dictionaryOfResults.keys()):
    	f.write(" " + dictionaryOfResults["given-names"] + '<br>' + '\n')

    if('abstract' in dictionaryOfResults.keys()):
    	if(len(dictionaryOfResults['abstract']) > 2000):
    		dictionaryOfResults['abstract'] = dictionaryOfResults['abstract'][:2000]
    		f.write("Abstract: " + dictionaryOfResults["abstract"] + "~"+ '<br>' + '\n')
    	else:
    		f.write("Abstract: " + dictionaryOfResults["abstract"] + '<br>' + '\n')

    f.write("Link: " + '<a href=' + '"' + dictionaryOfResults["self-uri"] + '"'+ ' target="_blank" '  + 
    	'>'+ dictionaryOfResults["self-uri"]  + '</a>' + ' '+ '\n')

    f.write(file)

    f.write("<hr>" + '<br>' + '\n' +'\n' )


def main():

	start = time.time()

	# Will store the words we will go through in here 
	terms = []
	# Don't want to process a word if we have already seen it
	uniqueTerms = set()

	# Pull out the topic words from the topic modeling file. 
	with open('dr_topics-RUN.txt') as f:
		for readData in f:
			newData = readData.split()
			terms.append(newData) #Add to list 
	f.close()

	# Go through list and process 1 at a time
	for items in terms:
		for word in range(1, len(items)):

			start1 = time.time()

			# Check to see if we have seen that word before
			if(items[word] not in uniqueTerms):
				f = open('Digital-Ricoeur-JStor-'+ items[word] +'.html', 'w+', encoding='utf-8')
				createHtmlFiles(items[word],f)
				findXmlFile(items[word],f)   
				f.write('  ' + '</body>' + '\n')
				f.write('</html>')

				# write counter here since it doesn't like it if I put this into another func
				with open('Digital-Ricoeur-JStor-'+ items[word] +'.html','r') as f:
					data = f.readlines()
					data[9] = data[9].replace('###',str(globalBook))
					data[10] = data[10].replace('!!!',str(globalJournal))

				with open('Digital-Ricoeur-JStor-'+ items[word] +'.html', 'w') as f:
					f.writelines(data) 

				f.close()    
				end1 = time.time()
				print("Time to auto-gen page for " + str(items[word]) + ": " + str(end1-start1) + " secs ")
				uniqueTerms.add(items[word])

			else:
				print("Already made the file for: ", items[word])
				continue	


	end = time.time()
	print("Overall Time: " + str((end-start)/3600.00) + " hours ")

if __name__ == "__main__": main()
