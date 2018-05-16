'''
By Alessandra Laurent

This version of the function uses the Stanford NER Tagger, which returns more accurate results than NLTK's built in NE Chunker.

The classifier must be downloaded from: https://nlp.stanford.edu/software/CRF-NER.shtml
Java Developer Kit must also be downloaded.

The path for both of these may have to be modified accordingly in order for the code to function.

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


#This function uses the Stanford NER Tagger to find names in a text file and returns a list of all names in order of appearance
def extract_names(file):
    
    #Tokenize + apply Stanford NER Tagger
    text = my_corpus.raw(file)
    tokens = nltk.word_tokenize(text) #includes punctuation as tokens
    #print(tokens)
    ne_tagged = st.tag(tokens)
    #print(ne_tagged)
    
    #Create a list of all identified person names, keeping track of each name's index in the text
    person_names = []
    person_counter = []
    for i, tag in enumerate(ne_tagged): #Go word by word
        if tag[1]=='PERSON': 
            person_names.append(tag[0])
            person_counter.append(i)
    #print(i, person_names, person_counter)
    
    #Merge consecutive names into a single string so that full names stay together
    all_names = []
    consecutive_name = False #Keep track of whether the name at current index should be concatenated with the one before it.
    for i in range(len(person_counter)-1):
        if not consecutive_name: 
            if person_counter[i]+1 == person_counter[i+1]:#Check for 2 consecutive counters
                consecutive_name = True #Next name should be concatenated to current one
                all_names.append(person_names[i])
            else:
                all_names.append(person_names[i])
                
        else:
            all_names[-1] = all_names[-1] + ' ' + person_names[i] #Check if the next name in list is consecutive
            if person_counter[i]+1 == person_counter[i+1]: #Check for 2 consecutive counters
                pass #consecutive_name stays True. Next name should be concatenated to current one
            else:
                consecutive_name = False #Next name is separate from this one           
    
    return all_names
    
#This function takes in a list of names, assigns last names to the preceding version of the corresponding name
def count_names(file):
    
    names_list = extract_names(file) #Get the complete name list from the prev function
    
    recent_names = [] #This list is to be regularly updated w/ the most recent version of a full(ish) name
    last_names = [] #This list serves as a tracker to find the indices of recent_names based on last names
    names_count = [] #This list will keep track of fullnames and the # of times cited thereafter
    
    for name in names_list:
        words = name.split(' ')
        if words[-1] in last_names:
            i = last_names.index(words[-1]) #Find the index of the name in recent_names
            if len(words) == 1:
                names_count.append(recent_names[i])
            else: #Update recent_names
                recent_names.pop(i)
                recent_names.insert(i, name)
                names_count.append(name)
                
        else: 
            recent_names.append(name)
            last_names.append(words[-1])
            names_count.append(name)
    names_agg = Counter(names_count).most_common()
    return names_agg
    
#Writes a list of tuples to a csv
def write_to_csv(file):
    names_agg = count_names(file)
    #Write the list to a csv file with names in one column and frequencies in the next
    col_file = open(file[:-4] + '.csv', 'w', encoding = 'utf-8', newline = '')#Name csv after the text file, removing .txt and adding .csv
    with col_file:
        col_writer = csv.writer(col_file)
        col_writer.writerows(names_agg)
    
    print('Writing complete')
    #Write the list to a csv file with names in one column and frequencies in the next
    col_file = open(file[:-4] + '_columns.csv', 'w', newline = '')#Name csv after the text file, removing .txt and adding .csv
    with col_file:
        col_writer = csv.writer(col_file)
        col_writer.writerows(allnames_sort)
    
    print('Writing complete')

    
#extract_network(my_corpus.fileids()[1])   

#Run the function for every file in the corpus
for book in my_corpus.fileids():
    print(book)
    write_to_csv(book)
