'''
By Alessandra Laurent

This version of the function uses the Stanford NER Tagger, which returns more accurate results than NLTK's built in NE Chunker.

The classifier must be downloaded from: https://nlp.stanford.edu/software/CRF-NER.shtml
Java Developer Kit must also be downloaded.

The path for both of these may have to be modified accordingly in order for the code to function.

**Remaining issue: compound last names such as "von Wright" are not aggregated with their full names bc both reside in the fullnames list**
'''

import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk.text import Text
from collections import Counter
import csv

from nltk.tag.stanford import StanfordNERTagger
st = StanfordNERTagger('../../../stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz', '../../../stanford-ner/stanford-ner.jar')

#Define the Java path
import os 
java_path = "C:/Program Files/Java/jdk-10/bin/java.exe"
os.environ['JAVAHOME'] = java_path

#Read in the corpus
corpus_root = '/../../data/books/'
my_corpus = PlaintextCorpusReader(corpus_root,'.*txt')


#This function uses the Stanford NER Tagger to find names in a text file and writes a reverse rank-ordered list of full names and frequencies to 2 csv formats
def extract_network(file):
    
    #Tokenize + apply Stanford NER Tagger
    text = my_corpus.raw(file)
    tokens = nltk.word_tokenize(text) #includes punctuation as tokens
    #print(tokens)
    ne_tagged = st.tag(tokens)
    #print(ne_tagged)
    
    allnames_agg = [] #aggregated list of all names with frequencies, to be assembled at the end
    fullnames = [] #list of consecutive names
    surnames = [] #list of single names   
    
    #Create a list of all identified person names, keeping track of each name's index in the text
    person_names = []
    person_counter = []
    for i, tag in enumerate(ne_tagged): #Go word by word
        if tag[1]=='PERSON': 
            person_names.append(tag[0])
            person_counter.append(i)
    #print(i, person_names, person_counter)
    
    #Go through the counter list: append names at indexes of consecutive numbers to fullnames, and names at indexes of non-consecutive numbers to surnames
    consecutive_name = False #Keep track of whether the name at current index should be concatenated with the one before it.
    for i in range(len(person_counter)-1):
        if not consecutive_name: 
            if person_counter[i]+1 == person_counter[i+1]:#Check for 2 consecutive counters
                consecutive_name = True #Next name should be concatenated to current one
                fullnames.append(person_names[i])
            else:
                surnames.append(person_names[i]) 
                
        else:
            fullnames[-1] = fullnames[-1] + ' ' + person_names[i] #Check if the next name in list is consecutive
            if person_counter[i]+1 == person_counter[i+1]: #Check for 2 consecutive counters
                pass #consecutive_name stays True. Next name should be concatenated to current one
            else:
                consecutive_name = False #Next name is separate from this one           
    
    #print(fullnames, surnames)
            
    #Create 2 lists of tuples of how many mentions per name
    fullnames_agg = Counter(fullnames).most_common()
    surnames_agg = Counter(surnames).most_common()
    #print(fullnames_agg)
    #print(surnames_agg)
    
    
    #Convert as many surnames as possible to full names
    allnames = []
    for surname in surnames_agg: #find full name match for each surname
        fullname_found = False
        #print('Surname:', surname[0])
        for fullname in fullnames_agg: #Look for the corresponding full name
            names = fullname[0].split(' ')
            #print(fullname[0], '-->', fullname_found)
            if surname[0] == names[-1]:
                fullname_found = True
                allnames.append((fullname[0], fullname[1] + surname[1])) #assign value to dic with full name instead
                #print(fullname[0], '-->', fullname_found)
                break #terminate the sub-loop once the first surname match has been found. agg list is already sorted by frequency, and most frequent is likely to be the correct version
        if not fullname_found: 
            allnames.append((surname)) #append remaining surnames w/o full names
    
    #Add remaining full names to the complete list
    for fullname in fullnames_agg:
        allnames_found = False
        for name in allnames:
            if fullname[0] == name [0]:
                allnames_found = True
                break #terminate the sub-loop once a match has been found
        if not allnames_found:
            allnames.append((fullname))
                
    allnames_sort = sorted(allnames,key=lambda x: x[1], reverse=True) #Sort in descending order to prep for excel output
    #print(allnames_sort)
    
    
    #Write the list to a csv file with names in one column and frequencies in the next
    col_file = open(file[:-4] + '_columns.csv', 'w', newline = '')#Name csv after the text file, removing .txt and adding .csv
    with col_file:
        col_writer = csv.writer(col_file)
        col_writer.writerows(allnames_sort)
    
    
    #Write the list to a 2nd csv file with names in one row and frequencies in the next
    #Create headings + set up format for the csv file
    row1_names = ['Book_Title', 'Year']
    book_data = file.split('_') #Add in book name and year, assuming a 'year_book-title.txt' format
    row2_count = [book_data[1][:-4], book_data[0]]
    
    #Transform the list into the proper format
    for thinker in allnames_sort:
        row1_names.append(thinker[0])
        row2_count.append(thinker[1])
    unique_thinkers = [row1_names, row2_count]
    
    #Write the list to a 2nd csv
    row_file = open(file[:-4] + '_rows.csv', 'w', newline = '')#Name csv after the text file, removing .txt and adding .csv
    with row_file:
        row_writer = csv.writer(row_file)
        row_writer.writerows(unique_thinkers)
    
    print('Writing complete')

    
#extract_network(my_corpus.fileids()[1])   

#Run the function for every file in the corpus
for book in my_corpus.fileids():
    extract_network(book)
