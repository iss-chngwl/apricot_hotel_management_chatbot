#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 20:22:20 2020

@author: jiahao
"""


import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import wordnet
from nltk.stem import SnowballStemmer, PorterStemmer, WordNetLemmatizer
import re
import nltk 
import copy
import spacy
from spacy.util import minibatch, compounding

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
# from spacy.lang.en.stop_words import STOP_WORDS
import matplotlib.pyplot as plt
from collections import Counter
plt.rcParams['savefig.dpi'] = 300

nlp = spacy.load("en_core_web_sm")

# import nltk
# nltk.download('vader_lexicon')

df = pd.read_excel(r'full_reviews.xlsx')
df = df[["review_text","classification"]]

#%% https://cloud.tencent.com/developer/article/1043114
# freq = nltk.FreqDist(extracted_words) 
# for key,val in freq.items(): 
#     print (str(key) + ':' + str(val))
    
# clean_tokens = extracted_words[:] 
# sr = stopwords.words('english')
# for token in extracted_words:
#     if token in stopwords.words('english'):
#         clean_tokens.remove(token)
        
# lemmatizer = WordNetLemmatizer()
# print(lemmatizer.lemmatize('increases'))

#%% ML Classifier
import sklearn
import nltk
import re 
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn import preprocessing
from sklearn import metrics
from sklearn.feature_selection import SelectKBest
from sklearn.feature_extraction.text import TfidfVectorizer #as vectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import chi2
from sklearn.metrics import precision_score, recall_score,f1_score
from sklearn.linear_model import LogisticRegression


#%%

from os import getcwd, chdir
import pandas as pd
import pickle as pk

from sklearn.feature_extraction.text import TfidfVectorizer

fpath = getcwd()
#Label conversion: Positive to 1,Negative to -1 
df_pos = df[(df["classification"] == 'Positive')]
df_neg = df[(df["classification"] == 'Negative')]
print (df_pos.head(3))
print (df_neg.head(3))

df_pos_list = []
for i,t in df_pos.iterrows():
    df_pos_list.append([t['review_text'].lower(), 1])

df_neg_list = []
for i,t in df_neg.iterrows():
    df_neg_list.append([t['review_text'].lower(), -1])

print(f"pos: {len(df_pos_list)} \nneg: {len(df_neg_list)}")
print(len(df_pos_list)/(len(df_pos_list)+len(df_neg_list)))


#build the two dataset
split = 0.9
trainset = df_pos_list[:int(split*len(df_pos_list))] + df_neg_list[:int(split*len(df_neg_list))]
testset = df_pos_list[int(split*len(df_pos_list)):] + df_neg_list[int(split*len(df_neg_list)):]

pk.dump(trainset, open(fpath+"/Data/trainset.pk", "wb"))
pk.dump(testset , open(fpath+"/Data/testset.pk", "wb"))


#%%Preprocessing 
# seperate the text with labels

X_train = [t[0] for t in trainset]
X_test = [t[0] for t in testset]

Y_train = [t[1] for t in trainset]
Y_test = [t[1] for t in testset]

#Vectorizer the sentences using Tfidf vale
#Make sure test data should be transformed using vectorizer learned from trainning data 
vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
train_vectors = vectorizer.fit_transform(X_train)
test_vectors = vectorizer.transform(X_test)

# same feature set
train_vectors.shape
test_vectors.shape

#%% NB model
clf_NB = MultinomialNB().fit(train_vectors, Y_train)
predNB = clf_NB.predict(test_vectors)
pred = list(predNB)

print(metrics.confusion_matrix(Y_test, pred))
print(metrics.classification_report(Y_test, pred))

#%% LogisticRegression
clf_ME = LogisticRegression(random_state=0, solver='lbfgs').fit(train_vectors, Y_train)
predME = clf_ME.predict(test_vectors)
pred = list(predME)
print(metrics.confusion_matrix(Y_test, pred))
print(metrics.classification_report(Y_test, pred))

#%%
#####KNN Classifier
def train_knn(X, y, k, weight):
    """
    Create and train the k-nearest neighbor.
    """
    knn = KNeighborsClassifier(n_neighbors = k, weights = weight, metric = 'cosine', algorithm = 'brute')
    knn.fit(X, y)
    return knn

kn = train_knn(train_vectors, Y_train, 3, 'distance')# distance weights - by inverse of distance
predKN = kn.predict(test_vectors)
pred = list(predKN)
print(metrics.confusion_matrix(Y_test, pred))
print(metrics.classification_report(Y_test, pred))

#%% SVM model

from sklearn import svm
from sklearn.svm import SVC

model_svm = SVC(C=5000.0, gamma="auto", kernel='rbf')
clr_svm = model_svm.fit(train_vectors, Y_train)

    
predicted = clr_svm.predict(test_vectors)
 
print(metrics.confusion_matrix(Y_test, predicted))
print(np.mean(predicted == Y_test) )
print(metrics.classification_report(Y_test, predicted))
