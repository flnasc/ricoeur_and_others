# Marty Dang 4/24/18

# This program will go through the list of jstore meta data and delete duplicate files

# It will first go through and sort files by size, grouping the same file size on together
# Then it will go through each list, compare the files in that group to each other to check
# for similarities. If it finds a similar one, it will delete one and keep the other 

import os
import filecmp
import time
from collections import defaultdict

sizeDictionary = defaultdict(list)
deletionPile = set()
deletions = 0

####################################################################################
# Deletion amount tracker
def incrementCounter():
	global deletions
	deletions += 1

####################################################################################

# find the file and folders first, determine size, and sort into appropriate list
def findFile():

	rootDir = '.'

	for dirName, subdirList, fileList in os.walk(rootDir):
		if(dirName == './jstor_metadata-Clean'):

		    for file in fileList:
		    	item = os.path.join(dirName, file)
		    	statinfo = os.stat(item)

		    	fileSorter(file, statinfo.st_size)
		    	
		    fileCompare(dirName)
		    delete(dirName)

####################################################################################
# make new lists and sort files into lists based on size
def fileSorter(file, size):
	# check if the size(key) exists already
	# if not make a new key for a new list
	# else insert it to the right one 
	global sizeDictionary

	sizeDictionary[size].append(file)
####################################################################################
# compare files and see if there is a duplicate, if there is print out the conflict
# compare the first file of list ot the rest and keep iterating through list till end
def fileCompare(dirName):
	global sizeDictionary

	for key, value in sizeDictionary.items():
		for currentFile in range(len(sizeDictionary[key])):
			for otherFile in range(currentFile+1, len(sizeDictionary[key])):
			    file1 = dirName + "/" + sizeDictionary[key][currentFile]
			    file2 = dirName +  "/" + sizeDictionary[key][otherFile]
			    if(filecmp.cmp(file1, file2) == True):
			    	global deletionPile
			    	print("Duplicate Found: ", file2)
			    	deletionPile.add(file2)

####################################################################################
# Goes through the deletion pile and deletes from the folder
def delete(dirName):
	global deletionPile
	for items in deletionPile:
		incrementCounter()
		print("Removed Duplicate File: ", items)
		os.remove(items)

####################################################################################

def main():

	start = time.time()

	findFile();

	end = time.time()

	print("Amount of duplicate files deleted: ", deletions)
	print("Overall Time: " + str((end-start)/3600.00) + " hours ")

	
if __name__ == "__main__": main()
					