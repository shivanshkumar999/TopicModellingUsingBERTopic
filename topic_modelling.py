# -*- coding: utf-8 -*-
"""Topic Modelling

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1N1XQJWtcocVFKtkYnZnEEpiuATu9y4-Y

## Scrape Data from Forbes International Site.


---



### Here I used 10 **Forbes** articles in the **Innovation** Domain
"""

import requests as r
from bs4 import BeautifulSoup
import pandas as pd

i=0
url = "https://www.forbes.com/innovation/?sh=78a7453c6834"

linklist = []
data = []

content1 = r.get(url)
soup1 = BeautifulSoup(content1.content, 'html.parser')
links = soup1.select('a._5ncu0TWl')
for link in links:
  linklist.append(link['href'])

for i in range(0,9):
  print("Parsing document - ", i)
  content2 = r.get(linklist[i])
  soup2 = BeautifulSoup(content2.content, 'html.parser')
  articles = soup2.select('p')
  for article in articles:
    data.append(article.text)

data

"""## Data Cleaning and PreProcessing"""

for i in range(0,len(data)-1):
  #Nullifying Small Articles
  if(len(data[i])<500):
    data[i]=""
  print(len(data[i]))
# Removing Null values
data = list(filter(None,data))

# Preprocessing Starts
import re
from wordcloud import STOPWORDS

for i in range(0,len(data)-1):
  # Lowercase
  data[i] = data[i].lower()
  # Remove Punctuation
  # data[i] = data[i].replace('.','')
  data[i] = data[i].replace(',','')
  data[i] = data[i].replace('!','')
  data[i] = data[i].replace('$','')
  print(data[i])

"""Tokenization and Stopword Removal"""

from nltk.tokenize import word_tokenize
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords

stopwords = set(stopwords.words('english'))
for i in range(0, len(data)-1):
  word_tokens = word_tokenize(data[i])
  final_data = [w for w in word_tokens if not w.lower() in stopwords]

for w in word_tokens:
  if w not in stopwords:
    final_data.append(w)

print(type(final_data))

!pip install BERTopic

from bertopic import BERTopic
model = BERTopic(verbose=True)

topics, probabs = model.fit_transform(final_data)

print(model.get_topic_freq())

# model.get_topic(0)
model.visualize_topics()

model.visualize_barchart()