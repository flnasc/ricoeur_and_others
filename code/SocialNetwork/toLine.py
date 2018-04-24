# py scrip that takes summary.csv and reformat it to better fit data structure needed for line graph
# Created by Do Yeun Kim

import pandas as pd

# Read in summary, sort data, and initialize output dataframe
data = pd.read_csv('./data/summary.csv', index_col=False)
sortedData = data.sort_values(by=['Thinker', 'Year'])
sortedData = sortedData.reset_index(drop=True)
lineGraph = pd.DataFrame(columns=['Title', 'Year'])
years = []


# Fetch the years and titles of Ricoeur's works
def detectYears():
    title = []
    for i in range(0, len(data.Year)):
        if i > 0:
            if years[-1] != data.Year[i]:
                years.append(data.Year[i])
                title.append(data.Title[i])
        else:
            years.append(data.Year[i])
            title.append(data.Title[i])
    
    print(years)

    for i in range(len(years)):
        lineGraph.loc[i] = [title[i], years[i]]



# Insert the Thinkers w/ appropriate frequency for each year/title
def insertThinkers():
    print(sortedData)
    curr_t = [0] * len(years)
    for i in range(0, len(sortedData.Year)):
        if i > 0:
            if sortedData.Thinker[i] != sortedData.Thinker[i - 1]:
                print(sortedData.Thinker[i - 1])
                print(curr_t)        
                lineGraph[sortedData.Thinker[i - 1]] = curr_t
                curr_t = [0] * len(years)
                for j in range(len(years)):
                    if sortedData.Year[i] == years[j]:
                        curr_t[j] = sortedData.Frequency[i]
                if i == len(sortedData.Year) - 1:
                    print(sortedData.Thinker[i])
                    print(curr_t)
                    lineGraph[sortedData.Thinker[i]] = curr_t


            else:
                for j in range(len(years)):
                    if sortedData.Year[i] == years[j]:
                        curr_t[j] = sortedData.Frequency[i]
                if i == len(sortedData.Year) - 1:
                    print(sortedData.Thinker[i])
                    print(curr_t)
                    lineGraph[sortedData.Thinker[i]] = curr_t

        else:
            for j in range(len(years)):
                if sortedData.Year[i] == years[j]:
                    curr_t[j] = sortedData.Frequency[i]
            if i == len(sortedData.Year) - 1:
                print(sortedData.Thinker[i])
                print(curr_t)
                lineGraph[sortedData.Thinker[i]] = curr_t

    # Done with creating the data frame, so proceed to output it as a csv
    lineGraph.to_csv('./data/lineGraph.csv', index=False)

detectYears() 
insertThinkers()
