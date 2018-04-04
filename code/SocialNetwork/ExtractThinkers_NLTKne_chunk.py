'''
This is the simpler version of the code to extract person names from the corpus and create csv files for each, using the built in NLTK NE chunker.

I also did not implement the first name recognition/elimination in this one, so the output is a lot messier but it runs a lot faster, and you don't need to have anything but NLTK downloaded.
'''

from nltk.corpus import PlaintextCorpusReader
from nltk.text import Text
corpus_root = '/Users/Alessandra Laurent/Documents/Icebox/Bowdoin Spring 2018/Digital Ricoeur/'
my_corpus = PlaintextCorpusReader(corpus_root,'.*txt')

from nltk import ne_chunk, pos_tag
from nltk.tree import Tree
from collections import Counter

#This function POS tags a text file and extracts an ordered list of names and frequencies for each
def extract_network(file):
    #POS tag text
    text = my_corpus.words(file)
    chunked = ne_chunk(pos_tag(text))
    
    #Extract list of people
    current_chunk = []
    for i in chunked:
        if type(i) == Tree: 
            if (i.label() == 'PERSON'):
                current_chunk.append(" ".join([token for token, pos in i.leaves()]))
   
    

    #Create ordered list of how many mentions per name
    agg_list = Counter(current_chunk).most_common()
    agg_list.insert(0, ('Thinker', 'Frequency')) #Insert headings for csv file
    #return agg_list

    #Write the list to a csv file with name in one column and frequency in the next
    myfile = open(file[:-4] + '.csv', 'w', newline = '')#Name csv after the text file, removing .txt and adding .csv
    with myfile:
        writer = csv.writer(myfile)
        writer.writerows(agg_list)
    print('Writing complete')
    

for book in my_corpus.fileids():
    extract_network(book)
