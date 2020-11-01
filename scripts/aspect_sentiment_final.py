#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 22:58:30 2020

@author: jiahao
"""


import pandas as pd
import spacy
from textblob import TextBlob
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
# from nltk.stem.snowball import SnowballStemmer

#%% Import data
df = pd.read_excel(r'full_reviews.xlsx')

# df = df.head(50)
#%% Prepare aspect list
hyps_room = list(set(
                [w for s in wn.synsets('bedroom')[0].closure(lambda s:s.hyponyms())
                        for w in s.lemma_names()]))
hyps_beverage = list(set(
                [w for s in wn.synsets('beverage')[0].closure(lambda s:s.hyponyms())
                        for w in s.lemma_names()]))  
hyps_food = list(set(
                [w for s in wn.synsets('food')[0].closure(lambda s:s.hyponyms())
                        for w in s.lemma_names()]))    
hyps_meal = list(set(
                [w for s in wn.synsets('meal')[0].closure(lambda s:s.hyponyms())
                        for w in s.lemma_names()]))   
# hyps_hotel = list(set(
#                 [w for s in wn.synsets('hotel')[0].closure(lambda s:s.hyponyms())
#                         for w in s.lemma_names()]))   
# hyps_restaurant = list(set(
#                 [w for s in wn.synsets('restaurant')[0].closure(lambda s:s.hyponyms())
#                         for w in s.lemma_names()]))  
hyps_value = list(set(
                [w for s in wn.synsets('value')[1].closure(lambda s:s.hyponyms())
                        for w in s.lemma_names()])) 
# hyps_sleep = list(set(
#                 [w for s in wn.synsets('sleep')[0].closure(lambda s:s.hyponyms())
#                         for w in s.lemma_names()])) 
hyps_location = list(set(
                [w for s in wn.synsets('location')[0].closure(lambda s:s.hyponyms())
                        for w in s.lemma_names()])) 
hyps_service = list(set(
                [w for s in wn.synsets('service')[0].closure(lambda s:s.hyponyms())
                        for w in s.lemma_names()]))
hyps_facility = list(set(
                [w for s in wn.synsets('facility')[0].closure(lambda s:s.hyponyms())
                        for w in s.lemma_names()]))

hyps_room = hyps_room + ['room', 'size', 'bathroom', 'shower', 'bath', 'sofa', 'fridge', 'wash', 'machine', 'rooms', 'kitchen', 'clean', 'dirty', 'toilet', 'dryer', 'view']
hyps_value = hyps_value + ['value', 'price', 'worth', 'low', 'high', 'cheap', 'expensive', 'rate', 'money', 'economical', 'reasonable', 'fee']
# hyps_sleep = hyps_sleep + ['sleep','bed','bedroom']
hyps_location = hyps_location + ['location', 'distance', 'distant', 'place', 'street', 'place', 'area', 'walk', 'station', 'metro', 'subway', 'train', 'mall', 'shopping', 'close', 'far', 'near', 'convenient', 'airport']
hyps_service = hyps_service + ['staff', 'wait', 'water', 'queue', 'people', 'service', 'lobby', 'housekeeping', 'desk', 'reception', 'desk', 'check', 'fast', 'request', 'help', 'polite', 'friendly', 'reliable', 'quick', 'slow']
hyps_facility = hyps_facility + ['facility', 'wifi', 'pool', 'swimming', 'gym', 'entertainment', 'internet', 'wireless', 'parking', 'damage', 'broken']
hyps_food = hyps_food + hyps_meal + hyps_beverage + ['food', 'drink', 'dish', 'wine', 'salad', 'breakfast', 'lunch', 'restaurant']

food = [word.replace("_"," ") for word in hyps_food]
value = [word.replace("_"," ") for word in hyps_value]
location = [word.replace("_"," ") for word in hyps_location]
service = [word.replace("_"," ") for word in hyps_service]
facility = [word.replace("_"," ") for word in hyps_facility]
room = [word.replace("_"," ") for word in hyps_room]

# entity & aspect categories
aspect = {
    "food": food,
    "value": value,
    "location": location,
    "service": service,
    "facility": facility,
    "room": room
    }

#%% Define funcitons
nlp = spacy.load('en_core_web_sm')
lemmatizer = WordNetLemmatizer()
lemmatizer.lemmatize('increases')
# others : will be everything else    
# Helper function for categorising aspects:
def aspectCat(sentence):
    category=[]
    for tok in sentence:
        tok = tok.text.lower()
        tok = lemmatizer.lemmatize(tok)
        for key, val in aspect.items():
            if tok in val: category.append(key)
    if len(category) == 0 : category.append("others")
    return category

def zero_division(n, d):
    return n/d if d else 0


#%% Process Aspect Sentiment Analysis

for i in range(len(df["review_text"])):
    doc = nlp(df["review_text"][i])
    # reviews_sent =[]
    food_count = 0
    value_count = 0
    location_count = 0
    service_count = 0
    facility_count = 0
    room_count = 0
    # other_count = 0
    
    food_senti = 0
    value_senti = 0
    location_senti = 0
    service_senti = 0
    facility_senti = 0
    room_senti = 0
    # other_senti = 0
    for idx, sentence in enumerate(doc.sents):
        cat = aspectCat(sentence)
        senti = TextBlob(sentence.text).sentiment.polarity
        # print(i, sentence, cat, senti)
        if "food" in cat:
            food_count += 1
            food_senti += senti
            # print(i, sentence, cat, senti)
        if "value" in cat:
            value_count += 1
            value_senti += senti
            # print(i, sentence, cat, senti)
        if "location" in cat:
            location_count += 1
            location_senti += senti
            # print(i, sentence, cat, senti)
        if "service" in cat:
            service_count += 1
            service_senti += senti
            # print(i, sentence, cat, senti)
        if "facility" in cat:
            facility_count += 1
            facility_senti += senti
            # print(i, sentence, cat, senti)
        if "room" in cat:
            room_count += 1
            room_senti += senti
            # print(i, sentence, cat, senti)
        # else:
        #     other_count += 1
        #     other_senti += senti
            # print(i, sentence, cat, senti)
            
    df.loc[df.index[i], 'aspect_food_score'] = (zero_division(food_senti,food_count)+1)/2
    df.loc[df.index[i], 'aspect_value_score'] = (zero_division(value_senti,value_count)+1)/2
    df.loc[df.index[i], 'aspect_location_score'] = (zero_division(location_senti,location_count)+1)/2
    df.loc[df.index[i], 'aspect_service_score'] = (zero_division(service_senti,service_count)+1)/2
    df.loc[df.index[i], 'aspect_facility_score'] = (zero_division(facility_senti,facility_count)+1)/2
    df.loc[df.index[i], 'aspect_room_score'] = (zero_division(room_senti,room_count)+1)/2
    # df.loc[df.index[i], 'aspect_other_score'] = (zero_division(other_senti,other_count)+1)/2
#%%
df.to_excel('aspect_reviews.xlsx', encoding='utf-8', index=False)
# df.to_excel('aspect_reviews.xlsx', encoding='utf-8', index=False)
