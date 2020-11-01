# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from tensorflow.keras.models import load_model
import re
import pandas as pd
from nltk.corpus import stopwords
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import numpy as np

def sentiment_pred(sentence, tokenizer, model):
    df = pd.DataFrame({'review_text': [sentence]})
    
    # pre-process data
    def remove_stopwords(input_text):
        stopwords_list = stopwords.words('english')
        # Some words which might indicate a certain sentiment are kept via a whitelist
        whitelist = ["n't", "not", "no"]
        words = input_text.split() 
        clean_words = [word for word in words if (word not in stopwords_list or word in whitelist) and len(word) > 1] 
        return " ".join(clean_words) 
    
    df['review_text'] = df['review_text'].map(lambda x: re.sub('[^A-Za-z\ 0-9 ]+', '', x))
    df['review_text'] = df['review_text'].map(lambda x: re.sub('[,\.!?]', '', x))
    df['review_text'] = df['review_text'].map(lambda x: x.lower())
    df['review_text'] = df['review_text'].apply(remove_stopwords)
    df.head()
    
    text_test = df['review_text']

    #tokenization
    maxlen = 827
    X_test = tokenizer.texts_to_sequences(text_test)
    X_test = pad_sequences(X_test, padding='post', maxlen=maxlen)
    
    #prediction
    y_pred = model.predict(X_test)
    
    if np.argmax(y_pred, axis=1) == 1:
        senti = "Positive"
    
    if np.argmax(y_pred, axis=1) == 0:
        senti = "Negative"
    
        
    return senti

