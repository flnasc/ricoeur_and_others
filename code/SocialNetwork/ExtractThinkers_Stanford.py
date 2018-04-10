'''
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


#This function uses the Stanford NER Tagger to find names in a text file and writes an rank-ordered list of names and frequencies to a csv
def extract_network(file):
    
    #Tokenize + apply Stanford NER Tagger
    text = my_corpus.raw(file)
    tokens = nltk.word_tokenize(text)
    ne_tagged = st.tag(tokens)
    #print(ne_tagged)
    
    thinker_names = []
    #Create a list of person names, keeping track of each name's index in the text
    person_names = []
    person_counter = []
    for i, tag in enumerate(ne_tagged): #Go word by word
        if tag[1]=='PERSON': 
            person_names.append(tag[0])
            person_counter.append(i)
        #print(i, person_names, person_counter)
            
        #If two words in a row are PERSONs, remove the first name
        if len(person_counter) > 1:
            if person_counter[-1] == person_counter[-2] + 1: #Check if indexes for the last two names directly follow each other
                person_names.pop(-2)
                person_counter.pop(-2)
            #print(person_names)
            
    #Add the final list of last names in the sentence to the master name list
    thinker_names.extend(person_names)
            
    #Create ordered list of how many mentions per name
    agg_list = Counter(thinker_names).most_common()
    #agg_list.insert(0, ('Thinker', 'Frequency')) #Insert headings for csv file
    #return agg_list
    
    #Transform the list to the proper format for the csv file
    row1_names = ['Book_Title', 'Year']
    book_data = file.split('_') #Add in book name and year, assuming a 'year_book-title.txt' format
    book_data = file.split('.')
    row2_count = [book_data[0], book_data[1]]
    for thinker in agg_list:
        row1_names.append(thinker[0])
        row2_count.append(thinker[1])
    thinkers_list = [row1_names, row2_count]

    #Write the list to a csv file with name in one column and frequency in the next
    myfile = open(file[:-4] + '_restructured.csv', 'w', newline = '')#Name csv after the text file, removing .txt and adding .csv
    with myfile:
        writer = csv.writer(myfile)
        writer.writerows(thinkers_list)
    print('Writing complete')

    
#extract_network(my_corpus.fileids()[1])   

#Run the function for every file in the corpus
for book in my_corpus.fileids():
    extract_network(book)
