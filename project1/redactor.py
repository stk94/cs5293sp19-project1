import sys
import re
import numpy as np
import pandas as pd
import nltk
from commonregex import CommonRegex
from nltk.corpus import wordnet
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktTrainer
import glob
import ntpath

#import project1
#from project1 import main

arguments = sys.argv
#print(arguments)

Input = []
Flags = []
Concept = []
Output = []
Stats = []

for i in range(0, len(arguments)):
    if arguments[i] == '--input':
        Input.append(arguments[i+1])
        i = i+1
    elif arguments[i] == '--concept':
        Concept.append(arguments[i+1])
        i = i+1
    elif arguments[i] == '--output':
        Output.append(arguments[i+1])
        i = i+1
    elif arguments[i] == '--stats':
        Stats.append(arguments[i+1])
        i = i+1
    else:
        if arguments[i].startswith('--'):
            Flags.append(arguments[i] [2:len(arguments[i])]) 

def Retrieve_Data(text_file):
    f = open(text_file,"r")
    data = f.read()
    return data

def Chunk_Data(data):
    tokenized = nltk.word_tokenize(data)
    tagged = nltk.pos_tag(tokenized)
    tree = nltk.ne_chunk(tagged, binary = False)
    return tree,tokenized

def Parsed_Text(data):
    parsed_text = CommonRegex(data)
    return parsed_text

def Retrieve_Person(tree,Flags):
    Person = []
    if 'names' in Flags:
        for node in tree:
            if type(node) is nltk.Tree:
                if node.label() == 'PERSON':
                    elements = node.leaves()
                    length = len(elements)

                    n = 0
                    str = ""
                    for x in range (0, length):
                        str = str + elements[x][n]
                        if x != length-1:
                            str = str + " "
                    Person.append(str)
    return Person

def Retrieve_Address(tree, parsed_text, Flags):
    Address = []
    if 'addresses' in Flags:
        for node in tree:
            if type(node) is nltk.Tree:
                if node.label() == 'GPE':
                    #print(type(node.leaves()))
                    #print(node.leaves())
                    elements = node.leaves()
                    length = len(elements)

                    n = 0
                    str = ""
                    for x in range (0, length):
                        str = str + elements[x][n]
                        if x != length-1:
                            str = str + " "
                    Address.append(str)

        Address.extend(parsed_text.street_addresses)

    return Address

def Retrieve_Phone(parsed_text, Flags):
    phones = []
    if 'phones' in Flags:
        phones.extend(parsed_text.phones)
    return phones

def Retrieve_Dates(parsed_text, Flags):
    Dates = []
    if 'dates' in Flags:
        Dates.extend(parsed_text.dates)
    return Dates

def Retrieve_Gender(tokenized):
    Gender = ["he", "she", "He", "She", "Mr.", "Mrs.", "Miss", "boys", "girls", "boy", "girl", "men", "women", "man", "woman"]
    Genders = []
    if 'genders' in Flags:
        for token in tokenized:
            if token in Gender:
                Genders.append(token)
    return Genders

def Fields_to_redact(Flags, Person, Address, Phones, Dates, Genders):
    Replace = []
    for element in Person:
        Replace.append(element)

    for element in Address:
        Replace.append(element)

    for element in Phones:
        Replace.append(element)

    for element in Dates:
        Replace.append(element)

    for element in Genders:
        Replace.append(element)

    return Replace


def Generate_Similar_Concept_Words(concept):
    synonyms = []
    syn = wordnet.synsets(concept)
    Syn_length = len(syn)
    #syn[0]
    for i in range(0,Syn_length):
        lemmas = syn[i].lemmas()
        #print(lemmas)
        Lemma_length = len(lemmas)
        for j in range(0,Lemma_length):
            synonym = (lemmas[j].name()).lower()
            #print(type(synonym))
            if synonym not in synonyms:
                synonyms.append(lemmas[j].name())
    return synonyms

def Tokenize_Sentenses(data):
    trainer = PunktTrainer()
    trainer.INCLUDE_ALL_COLLOCS = True
    tokenizer = PunktSentenceTokenizer(trainer.get_params())
    Sentences = tokenizer.tokenize(data)
    return Sentences

def Retrieve_Concept_Sentences(Sentences, Similar_Words, Replace):
    for j in range(0,len(Sentences)):
        for i in range(0,len(Similar_Words)):
            if Similar_Words[i] in Sentences[j]:
                Replace.append(Sentences[j])

    #print("Replace =", Replace)
    return Replace

def Redact(Replace,data):
    for j in range(0,len(Replace)):
        if Replace[j] in data:
            data = re.sub(Replace[j], '\u2588', data, 1)
    return data

def Output_Files(data,Location):
    f = open(Location,"w")
    f.write(data)
    f.close()

def Stats_Display(data, File_Name, Person, Address, Phones, Dates, Genders, Replace, Flags, Concept, Stats):
    Information = ''

    Information = ('File Name:{0}\n'.format(File_Name))
    Information += ('Redaction Flags used are {0}\n'.format(Flags))
    Information += ('Concept used is {0}\n'.format(Concept[0]))
    Information += ('Number of names redacted are {0}\n'.format(len(Person)))
    Information += ('Number of words/phrases redacted for Address are {0}\n' .format(len(Address)))
    Information += ('Number of phone numbers  redacted are {0}\n' .format(len(Phones)))
    Information += ('Number of Dates redacted are {0}\n' .format(len(Dates)))
    Information += ('Number of words redacted for Gender are {0}\n' .format(len(Genders)))
    concept_sentences = len(Replace) - len(Person) - len(Address) - len(Phones) - len(Dates) - len(Genders)
    Information += ('Number of sentences redacted due to concept are {0}\n' .format(concept_sentences))
    
    
    f = open('stats/stats.txt',"a")
    f.write(Information)
    f.close()
    
    if Stats[0] == 'stderr':
        sys.stderr.write(Information)
    
    if Stats[0] == 'stdout':
        sys.stdout.write(Information)

empty = ''
f = open('stats/stats.txt',"w")
f.write(empty)
f.close()

TextFiles = []
for path in Input:
    TextFiles.extend(glob.glob(path))

for File_Name in TextFiles:

    data = Retrieve_Data(File_Name)
    tree,tokenized = Chunk_Data(data)
    parsed_Text = Parsed_Text(data)

    Person = Retrieve_Person(tree, Flags)
    Address = Retrieve_Address(tree, parsed_Text, Flags)
    Phones = Retrieve_Phone(parsed_Text, Flags)
    Dates = Retrieve_Dates(parsed_Text, Flags)
    Genders = Retrieve_Gender(tokenized)

    Replace = Fields_to_redact(Flags, Person, Address, Phones, Dates, Genders)

    Sentences = Tokenize_Sentenses(data)
    Similar_Words = Generate_Similar_Concept_Words(Concept[0])
    Replace = Retrieve_Concept_Sentences(Sentences, Similar_Words, Replace)


    data = Redact(Replace,data)
    File_Name = ntpath.basename(File_Name)
    File_Name = File_Name[:-4]
    Location = Output[0] + File_Name + '.redacted'

    Output_Files(data, Location)
    #Location = Stats[0]
    #print(Stats)
    Stats_Display(data, File_Name, Person, Address, Phones, Dates, Genders, Replace, Flags, Concept, Stats)
    


