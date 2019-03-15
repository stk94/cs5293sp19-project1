# cs5293sp19-Project1

Name: SAI TEJA KANNEGANTI
Date: 03/14/2019


Description of the Project:
https://oudalab.github.io/textanalytics/projects/project1


Execution of code: (directions on how to install and use the code)

1. My code is present in Redactor.py.
2. Will run the code using the command below:
	pipenv run python redactor.py --input '*.txt' \
                    --input 'otherfiles/*.txt' \
                    --names --dates --addresses --phones --genders\
                    --concept 'kids' \
                    --output 'files/' \
                    --stats stderr

3. By running above command, redactor.py will be executed.
4. Each run of the above command will take different redaction flags and concept words along with different input text files and create output files that has redacted data and these files are with .redacted extension. Will create a stats file where ststistics of redaction are mentioned.


Approach:

I have done this project in 5 steps. 
	1. Splitting command line arguments into different fields
	2. Retrieve data
	3. Chunking and parsing data
	4. Retrieve Flags
	5. Retrieve sentences based on concept word
	6. Redaction
	7. Output files
	8. Stats

1. Splitting command line arguments into different fields: 
	a. Used sys package and able to extract path of input files, path of output files and stats file.
	b. Able to extract fields and flags 

2. Retrieve Data:
	a. Made a list of all text files that need to be redacted.
	b. Each file is accessed as per index in the list.
	c. Data is read by opening file in read mode.

3. Chunking and parsing data:
	a. used nltk. word_tokenize to tokenize to words and PunktSentenceTokenizer to tokenize to sentences.
	b. Parsed text

4. Retrieve Flags:
	a. data after tokenized by words to retrieve names and also for addresses.
	b. commonregex is used to identify words that belong to dates, phones, address(Street number)

5. Retrieve sentences based on concept word
	a. Used wordnet to identify similar words.
	b. Identify sentence if any of above mentioned word lies in Sentence

6. Redaction:
	a. A list contains all redaction words due to flags and concept.
	b. These words/sentences are redacted from original data

7. Outputfiles:
	a. Based on location given in command prompt, all output files have .redacted extension with same name as text file.

8. Stats:
	a. Gives number of phrases/words redacted for each flag and concept.
   

Inspiration:
1. https://www.youtube.com/watch?list=PLQVvvaa0QuDfRO5bQFLcVgvIOIhNUZpZf&v=5heWVbihZrM
2. https://github.com/madisonmay/CommonRegex
3. https://stackoverflow.com/questions/3308102/how-to-extract-the-n-th-elements-from-a-list-of-tuples
4. https://www.oreilly.com/library/view/python-text-processing/9781849513609/ch01s07.html
5. https://www.geeksforgeeks.org/get-synonymsantonyms-nltk-wordnet-python/
6. https://nlpforhackers.io/splitting-text-into-sentences/
7. https://www.tutorialspoint.com/python/python_command_line_arguments.htm
8. https://www.tutorialspoint.com/python/string_startswith.htm
9. https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
10. http://www.itsyourip.com/scripting/python/python-remove-last-n-characters-of-a-string/
11. https://stackoverflow.com/questions/5214578/python-print-string-to-text-file
12. https://stackoverflow.com/questions/5574702/how-to-print-to-stderr-in-python

People contacted:

Gowtham Teja Kanneganti, gowthamkanneganti@ou.edu, He mentioned me about package CommonRegex, Discussed Passing multiple arguments from command line, Both watched same tutorial in youtube for named entities, I am actually appending lists but he told extend lists will also be helpful.

Assumptions:
1. For displaying stats, I am always displaying stats to /stats/stats.txt. It will also display stats to stderr or stdout but not to a file if mentioned through command line.  
2. I assumed commonregex identifies all dates, street address, phone numbers.

