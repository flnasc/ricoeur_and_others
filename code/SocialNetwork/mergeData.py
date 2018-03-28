# py script that merges .csv files from Ricoeur's work and appends the name of the work 
# and year the work is published
# Created by Do Yeun Kim

import pandas as pd
import glob, os
import numpy as np

# define path and initialize output 
# right now, the output file is named as summary.csv, so we don't want to be reading in a file
# whose name begins with "summary." This is done through files, which are all .csv files other
# than those beginning with "summary."
os.chdir("./data")
summary = pd.DataFrame([])
files = glob.glob('[!summary]*.csv')

# Iterate through the .csv files in the path, extract name of the work and year published
# then merge the data, tagging for name and year
for counter, file in enumerate(files):

# Get file name and remove file extension
    fname = os.path.splitext(os.path.basename(file))
    fname = fname[0].split("_")
    name = []

# Extract year of publication, and join the rest of file name 
# The naming convention for .csv files is: [year published]_[name of work, separated by "_"].csv
    for counter, i in enumerate(fname):
        if (counter == 0):
            year = int(i)
        else:
            name.append(i)
    name = ' '.join(name)

# Read in the csv file, add Year and Title column, and populate them
# Once each work has been read, merge them into summary
    workdf = pd.read_csv(file, skiprows=0, usecols=[0,1])
    workdf['Year'] = workdf.apply(lambda row: year, axis = 1)
    workdf['Title'] = workdf.apply(lambda row: name, axis = 1)
    summary = summary.append(workdf)

# Output merged .csv file as .summary.csv
summary = summary.sort_values(by=['Year', 'Thinker'])
summary.to_csv("./summary.csv", index = False)

