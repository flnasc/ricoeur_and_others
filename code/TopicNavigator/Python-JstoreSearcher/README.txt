Marty Dang 5/25/18

Purpose: 

2 Programs:

  1. ricoeurSearcher.py

  This program takes a search term and then goes through the jstor metadata and 
  sees if that term and the word "Ricoeur" is mention in that metadata. The metadata is comprised of
  books and journals. 

  2. JstoreSearcher.py

  This program is just like the one above except it searches for only the key term and not for "Ricoeur"

To Use:

  1) Just run ricoeurSearcher.py and JstoreSearcher.py

Program Structures

  1) incrementBook and  incrementJournal - increment the counters to keep track of search results
  2) clearCounters - clears the counters
  3) createHtmlFiles(term,f) - Takes in the term, and f (html file we are writing to) and creates
                               the basic heading information.
  4) findXmlFile(term,f): - Takes in the term, and f (html file we are writnig to) and walks the
                            directory and figures out if the current xml file from the jstor metadata
                            is a book or journal and calls praseJournal or parseBook respectively
  5) parseJournalChapterXMLFile(term, item, file, f) - takes in the term, item (os path), the file and
                                                       f again. It uses element tree to go through and
                                                       parse the xml file. Look for key attributes and
                                                       store it in a dictionary so we can write to the
                                                       html files later. 
  6) parseBookChapterXmlFile(term, item, file, f) - Takes in the same as above and does the same except
                                                    for books. Note that there is a book section and a
                                                    section for book chapters. 
  7) addBooktoHtmlFile(dictionaryOfResults, file, term, f) - Params are same except that 
                                                             dictionaryOfResults is the stuff we want,created
                                                             from the parsing functions
  8) addChapterToHtmlFile - Same as 7)
  9) addJournalToHtmlFile - Same as 7 and 8) 
  10) main function - we get key words from the dr_topic-RUN.txt file. 

Limtiations/Bugs

It takes a while to create all the files (25 seconds per). Perhaps we can find a way to make it quicker?

