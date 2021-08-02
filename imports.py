!pip install praw 
!pip install emoji
!pip install yfinance



import praw
from praw.models import MoreComments
import pandas as pd
import nltk
import spacy
import emoji 
import re
import en_core_web_sm
import time

import yfinance

import seaborn as sns
import matplotlib.pyplot as plt

from nltk.tokenize import word_tokenize, sent_tokenize, RegexpTokenizer
from nltk.sentiment import sentiment_analyzer, vader
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import stopwords, subjectivity
from nltk.stem import WordNetLemmatizer
from nltk import FreqDist
from nltk.corpus import wordnet as wn

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('vader_lexicon')
nltk.download('sentiwordnet')
nltk.download('subjectivity')
