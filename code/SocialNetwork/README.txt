This is the README file for the Social Network branch of Ricoeur and Others project, under Digital Ricoeur Project.

1. Naming Convention for Books
	[Publication Year]_[Book-Title-Connected-with-Dashes].txt
	The books can be found in /ricoeur_and_others/data/books

2. Workflow
	All codes associated with Social Network branch are found here, in /ricoeur_and_others/code/SocialNetwork
	The work flow for the visualization is as follows:
		1. Python scripts (ALESSANDRA PLEASE FILL THIS PART)
		2. Use mergeData.py to combinte the output files into one for the bargraph, named barGraph.csv
		3. Use toLine.py to reformat the output of mergeData.py as lineAVG.csv (toLine.py fetched barGraph.csv as input file)
		4. DR_SN_barGraph.js reads in barGraph.csv and visualizes the data as the bargraph and DR_SN_lineGraph.js reads in lineGraph.csv and visualizes the data as a line chart. Note that DR_SN_barGraph.js is linked to DR_barGraph.html and that DR_SN_lineGraph.js is linked to DR_lineGraph.html
