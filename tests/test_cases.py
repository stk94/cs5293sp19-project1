import pytest
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


import project1
from project1 import redactor

Input = []
Flags = ['dates', 'phones']
Concept = []
Output = []
Stats = []

data = "I am Sai Teja. I went to Houston on 03/01/2019. I met Gowtham and he resides in 1003 E Brooks St, Apt D, Houston, 73071. I usually contacts him by 4059687594 or 4059687596. We were friends from when we are kids."

"""
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
"""

def test_Chunk_Data():
    tree,tokenized = redactor.Chunk_Data(data)
    assert tokenized is not None

def test_parsed_Data():
    parsed_text = redactor.Parsed_Text(data)

    assert parsed_text is not None 



def test_dates():
    parsed_text = redactor.Parsed_Text(data)
    dates = redactor.Retrieve_Dates(parsed_text, Flags)

    assert dates is not None


def test_names():
    parsed_text = redactor.Parsed_Text(data)
    phones = redactor.Retrieve_Phone(parsed_text, Flags)

    assert phones is not None
