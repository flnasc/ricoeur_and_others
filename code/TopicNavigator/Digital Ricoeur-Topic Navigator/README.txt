Marty Dang 5/24/18

Files in this folder:

Digital Ricoeur-Topic Navigator - the html file output
dr_topics - the old list
dr_topics-RUN - Use this to run the htmlAutoGenerator
htmlAutoGenerator - the program
README - the readme

Purpose: 

Takes in a file that contains topic words and creates an html page that lists them and the links
to the search on the Paul Riceour Site.

To Use:

1) Run htmlAutoGenerator.py on the command prompt
2) When prompted enter in "dr_topics-RUN.txt"
3) File generated will be titled "Digital Ricoeur-Topic Navigator"

Bugs/Limitations:

1) There is a slight but if the title of a group of topics is more then one word.
For example, a title of "Truth" would work correctly but a topic title like 
"Truth and Word", the program would create it incorrectly as just "Truth" instead of 
the whole thing. This should be an easy fix. 