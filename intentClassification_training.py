# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 16:02:38 2020

@author: chngweil
"""

import pandas as pd
intents = pd.read_csv('intents.csv', header=None)
intents.columns = ['questions','intent']

intentslist = list(intents.to_records())
# entity_country_city_hotel
entities = ['country','city','hotel']
intentslist1 = [[q.replace("<entity_country_city_hotel>",entity),l] if not q.find("<entity_country_city_hotel>") == -1 else [q,l] for entity in entities  for i,q,l in intentslist]


# entity_aspect
entities = ['housekeeping', 'location', 'area', 'breakfast', 'food']
intentslist2 = [[q.replace("<entity_aspect>",entity),l] if not q.find("<entity_aspect>") == -1 else [q,l] for entity in entities  for q,l in intentslist1]

# KPI
kpis = ["gri","sentiment score"]
intentslist3 = [[q.replace("<KPI>",kpi),l] if not q.find("<KPI>") == -1 else [q,l] for kpi in kpis  for q,l in intentslist2]


intentsdf2 = pd.DataFrame(intentslist3).drop_duplicates()    
intentsdf2.columns = ['questions', 'intent']
intentsdf2.groupby('intent').count()



import nltk
from nltk.corpus import stopwords
newstopwords= ['the','is','are', 'and'] #+ stopwords.words("English")
WNlemma = nltk.WordNetLemmatizer()


def pre_process(text):
    tokens = nltk.word_tokenize(text)
    tokens=[WNlemma.lemmatize(t) for t in tokens]
    tokens=[word for word in tokens if word not in newstopwords]
    text_after_process=" ".join(tokens)
    return(text_after_process)

#Apply the function on each document
intentsdf2['questions2'] = intentsdf2['questions'].apply(pre_process)

intentsdf2.head()


#####################Data Split and Create DTM
#split the data into training and testing
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(intentsdf2.questions2, intentsdf2.intent, test_size=0.3, random_state=12)

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import Pipeline
import numpy as np
from sklearn import metrics 
count_vect = CountVectorizer()

from sklearn import svm
from sklearn.svm import SVC

calibratedSVM = CalibratedClassifierCV(svm.LinearSVC(C=2.0), method='sigmoid', cv=5)

from sklearn.linear_model import SGDClassifier
tf = TfidfVectorizer(use_idf=True,ngram_range=(1,2))
tf.fit(X_train)
text_clf = Pipeline([('tfidf', TfidfVectorizer(use_idf=True,ngram_range=(1,2))),
                      ('clf', calibratedSVM)
                    ])
text_clf.fit(X_train, y_train) 
    
predicted = text_clf.predict(X_test)
 
print(metrics.confusion_matrix(y_test, predicted))
print(np.mean(predicted == y_test) )
print(metrics.classification_report(y_test, predicted))

res =pd.DataFrame()
res['X'] = X_test.reset_index(drop=True)
res['Y'] = y_test.reset_index(drop=True)
res['predicted'] = predicted

reswrong = res[res['Y']!=res['predicted']]

joblib.dump(text_clf, 'model_tfidf_svmClf.sav')
