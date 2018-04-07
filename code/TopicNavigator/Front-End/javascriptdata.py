# Marty Dang 3/13/18

# This program does the followering:
# 1. Takes in an input of a .txt file, as command prompt
# 2. It then scans and picks out the individual words
# 3. Outputs those words to another file
# 4. In that other file, it should append the link of the website with the word
# 5. Append all of that to a href tag for html

#Be sure to have your input text file in the same location as this program!

# Read/Open the file, outputs a list of lists 
def processFile():
    
    clean_file = []
    
    file = "dr_topics.txt"
        
    with open(file) as f:
        for read_data in f:
            #read_data = f.readline() #read in lines as strings
            read_data = read_data.split() #gets rid of spaces, tab chars etc
            read_data = read_data[2:] #gets rid of first two numbesr
            clean_file.append(read_data) #Add to list
    f.closed
    
    return clean_file
################################################################################

#Will create a file with just key words and link them 
def createNewFile(inputFile):
    Topics = []
    all_terms = []
    count = 0
    #loop through and find words
    for topic in inputFile:
        count += 1
        Topics.append(topic[0].title())
        terms = []
            
        for word in range(len(topic)):
            terms.append(topic[word])
        all_terms.append(terms)

    f = open('Digital Ricoeur-Topic Navigator.txt','w') #create another file

    f.write('var topics = [')
    for i in range(count):
        f.write('"' + Topics[i] + '",')
    f.write(']\n')
    f.write('var all_items = [\n')
    for terms in all_terms:
        f.write('[')
        for term in terms:
            f.write('"' + term + '",')
        f.write(']\n')
    f.closed
################################################################################
# main function
def main():
    clean_file = processFile()
    clean_file = createNewFile(clean_file)
    print("Completed converting the file.")

if __name__ == "__main__": main()
