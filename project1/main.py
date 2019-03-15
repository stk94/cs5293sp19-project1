import sys
import re
import numpy as np
import pandas as pd
import nltk
from commonregex import CommonRegex
from nltk.corpus import wordnet
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktTrainer
import glob


def Retrive_Data(text_file):
    f = open(text_file,"r")
    data = f.read()
    return data

def Chunk_Data(data):
    tokenized = nltk.word_tokenize(data)
    tagged = nltk.pos_tag(tokenized)
    tree = nltk.ne_chunk(tagged, binary = False)
    return tree,tokenized

def Retrieve_Person(tree):
    Person = []
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

def Parsed_Text(data):
    parsed_text = CommonRegex(data)
    return Parsed_Text

def Retrieve_Address(tree, parsed_text):
    Address = []
    for node in tree:
        if type(node) is nltk.Tree:
            if node.label() == 'GPE':
                print(type(node.leaves()))
                print(node.leaves())           
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

def Retrieve_Phone(parsed_text):
    phones = []
    phones.extend(parsed_text.phones)
    return phones

def Retrieve_Gender(tokenized):
    Gender = ["he", "she", "He", "She", "Mr.", "Mrs.", "Miss", "boys", "girls", "boy", "girl", "men", "women", "man", "woman"]
    Genders = []
    for token in tokenized:
        if token in Gender:
            Genders.append(token)
    return Genders

def Fields_to_redact:
    Replace = []
    for element in Dates:
    #print(element)
        Replace.append(element)

    for element in Genders:
    #print(element)
        Replace.append(element)

    for element in Address:
    #print(element)
        Replace.append(element)

    for element in Person:
    #print(element)
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

def Retrieve_Concept_Sentences(Sentences, Replace):
    for j in range(0,len(Sentences)):
        for i in range(0,len(synonyms)):
            if synonyms[i] in Sentences[j]:
                Replace.append(Sentences[j])
    return Replace

