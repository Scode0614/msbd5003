import pandas as pd
import numpy as np
import re
from nltk.tokenize import WordPunctTokenizer
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
import string

nltk.download('stopwords')
sw = stopwords.words('english')
nltk.download('wordnet')

tok = WordPunctTokenizer()

pat1 = r'@[A-Za-z0-9_]+'
pat2 = r'https?://[^ ]+'
combined_pat = r'|'.join((pat1, pat2))
www_pat = r'www.[^ ]+'
negations_dic = {"isn't":"is not", "aren't":"are not", "wasn't":"was not", "weren't":"were not",
                "haven't":"have not","hasn't":"has not","hadn't":"had not","won't":"will not",
                "wouldn't":"would not", "don't":"do not", "doesn't":"does not","didn't":"did not",
                "can't":"can not","couldn't":"could not","shouldn't":"should not","mightn't":"might not",
                "mustn't":"must not"}

neg_pattern = re.compile(r'\b(' + '|'.join(negations_dic.keys()) + r')\b')

def tweet_cleaner(text):
  try:
      bom_removed = text.decode("utf-8-sig").replace(u"\ufffd", "?")
  except:
      bom_removed = text
  stripped = re.sub(combined_pat, '', bom_removed)
  stripped = re.sub(www_pat, '', stripped)
  lower_case = stripped.lower()
  neg_handled = neg_pattern.sub(lambda x: negations_dic[x.group()], lower_case)
  letters_only = re.sub("[^a-zA-Z]", " ", neg_handled)
  # During the letters_only process two lines above, it has created unnecessay white spaces,
  # I will tokenize and join together to remove unneccessary white spaces
  words = [x for x  in tok.tokenize(letters_only) if len(x) > 1]
  # words = [x for x  in tok.tokenize(neg_handled) if len(x) > 1]
  return (" ".join(words)).strip()


word_tokenizer = TweetTokenizer(strip_handles=True, preserve_case=False, reduce_len=True)
def remove_punc_and_stopword(text):
  punc_removed = [word for word in text if word not in string.punctuation]
  punc_removed = ''.join(punc_removed)
  punc_removed = word_tokenizer.tokenize(punc_removed)
  vocabularies = []
  for token in punc_removed :
    if token.lower() not in sw:
      vocabularies.append(token.lower())
  return vocabularies

def rem_single_characters_and_http(lst):
  outputlst = []
  for word in lst:
    if word.startswith("http") == False:
      temp = re.sub('[^a-zA-Z ]+',' ', word) 
      temp=re.sub("&lt;/?.*?&gt;",' ',temp)
      temp=re.sub("(\\d|\\W)+"," ",temp)
      if(len(temp)<=3):
        outputlst.append(' ')        
      else:
        outputlst.append(temp)
  return outputlst

filter_words = ['covid']
def lemmatizationFunct(x):
  lemmatizer = WordNetLemmatizer()
  finalLem = []
  for s in x:
    vab = lemmatizer.lemmatize(s)
    if vab.startswith(" ") == False and vab not in filter_words:
      finalLem.append(vab)
    # finalLem.append(vab)
  return finalLem


def joinTokensFunct(x):
  x = " ".join(x)
  return x

def removecharacters(text):   
  text=text.strip()
  text = re.sub('\s+', ' ', text).strip()
  return text


def process(text):
  text = tweet_cleaner(text)
  text = remove_punc_and_stopword(text)
  text = rem_single_characters_and_http(text)
  text = lemmatizationFunct(text)
  text = joinTokensFunct(text)
  text = removecharacters(text)
  return text