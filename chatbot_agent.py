# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 23:08:34 2020

@author: chngweiluen
"""
import os
import numpy as np
import json
from itertools import compress
import spacy
import pandas as pd
import joblib
import pickle
from datetime import datetime
from datetime import timedelta
import dateparser
import re
import nltk
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
from action_modules import *
#from sentiment_analysis import *


class agent_jarvis2():
        
    propertyMappingFilename = 'Property Mapping.xlsx'
    intents_file_list = ['intent_greeting.json','intent_change.json','intent_reset.json',
                         'intent_list_top_entity.json','intent_list_worst_entity.json',
                         'intent_list_good_aspect.json','intent_list_bad_aspect.json',
                        'intent_query_performance.json']
    standaranswerFilename = 'standard_answer.json'
    intentDetModelFilename = 'model_tfidf_svmClf.sav'
    sent_tokenizerFilename = 'tokenizer.pickle'
    sent_modelFilename = 'cnn_model.hdf5'
    databasefilename = 'aspect_reviews.csv'
    
    intents = list()       # load all intents
    try:
        for f in intents_file_list:
            with open(os.path.join('intents',f)) as json_file:
                intents.append(json.load(json_file))
        print('Successfully load intents json files')
    except:
        raise ValueError('Intent json files broken or missing')
        
    # ----------------------------------------------------------
    try:
        with open(standaranswerFilename) as json_file:
            stand_ans = json.load(json_file)
        print("Successfully load standard answer file")
    except: 
        raise ValueError("standard answer json file broken or missing")
 
    # -------pre-load property matching list--------------------- 
    try:
        prop_map = pd.read_excel(os.path.join('data', propertyMappingFilename))
        hotel_list = prop_map['Property Name'].tolist()
        country_list = prop_map['Country'].tolist()
        city_list = prop_map['City'].tolist()
        brand_list = prop_map['Brand'].tolist()
        mentioned_word_list = ['mentioned_country','mentioned_hotel',
                                    'mentioned_city','mentioned_brand',
                                    'mentioned_gri','mentioned_sentiment'] 
        print("Successfully load property mapping files")
    except:
        raise ValueError('Property mapping file broken or missing')    
    
    # -----------preload model-----------------------------------
    # load the intent classifcation model
    try:
        intentDetectionModel = joblib.load(open(os.path.join('models', intentDetModelFilename), 'rb'))
        print("Intent classification model intialization complete!")
    except:
        raise ValueError("Intent Classification Model broken")
        
    # ------------load the sentiment tokenzier model --------------
    try:
        with open(os.path.join('models', sent_tokenizerFilename), 'rb') as handle:
            sent_tokenizer = pickle.load(handle)
        print("Sentiment tokenizer loaded successfully")
    except:
        raise ValueError("sentiment tokenizer loading fail")
    
    # ------------load the sentiment classification model ---------
    #try:
    #    sent_model = load_model(sent_modelFilename)
    #    print("Sentiment model initialization complete!")
    #except:
    #    raise ValueError("Sentiment model broken")
    
    #---------load the required spacy model-----------------------
    try:
        nlp = spacy.load("en_core_web_sm") # pipeline: tagger, parser, ner
        print("Spacy NLU model intialization complete!")
    except:
        raise ValueError("Spacy en_core_web_sm model broken.")
        
    # ---------load properties data -------------------------------
    try:
        database = pd.read_csv(os.path.join('data', databasefilename), header=0, index_col=0,engine='python').reset_index()
        database['published_date'] = pd.to_datetime(database['published_date'])
        print("Properties Database loaded succesfully")
    except:
        raise ValueError("Properties Database loading fail ")
        
    print("chatbot data and model laoding completed ")
    
    def __init__(self):         
             
        self.state=0                # 0 to identify intent,1 to fill slots, 2 fulfilled, 3 error
        self.i_counter=0            # to monitor error for intent identification
        self.s_counter=0            # to monitor error for slot filling 
        self.intent=None            # so store current intent 
        self.suspect_intent = None  # intent to be confirmed
        self.suspect_intent_text_tag = None # temporarily store intent to be confirmed text_tag
        self.slots=dict()           # to store slots 
        self.change_slot_request=0  # flag for slot changing on-going
        self.score_threshold = 0.6
        self.datanow = datetime(2020, 6,30)
        
        print("Chatbot Initialized")
        
    def nlu(self,input_message):
        '''
        nlu module to detect intents and possible slots
        '''
        entities = list()
        tokens = list()
        nlu_text_tag = list()
        
        # NLU process
        nlu_processed_text = self.nlp(input_message)
        
        # tokenization + lemmatization
        for token in nlu_processed_text:
            tokens.append(token.lemma_)
        
        # matching hotel list
        textngrams = list()
        for n in np.arange(3,5):
            a = ngrams(tokens,n)
            for i in a:
                textngrams.append((' '.join(i)).lower())

        ma = list()
        htl_tlist = list()
        for htl in self.hotel_list:
            htl_t = word_tokenize(htl)
            for n in np.arange(3,5):
                c = list(ngrams(htl_t, n))
                htl_tlist.append([(' '.join(item)).lower() for item in c])

        for d in htl_tlist:
            ma.append(bool(set(d).intersection(textngrams)))

        match = any(ma)
        resmatch1 = list(compress(self.hotel_list, ma[::2]))
        resmatch2 = list(compress(self.hotel_list, ma[1:][::2]))

        if match:
            mahotel = resmatch1[0] if resmatch1 else resmatch2[0]
            nlu_text_tag.extend([(mahotel, 'matched_hotel')])
        
        else:
        # matching country city and brand
            nlu_text_tag.extend([(t, 'matched_country') for t in tokens if t in self.country_list])
            nlu_text_tag.extend([(t, 'matched_city') for t in tokens if t in self.city_list])
            nlu_text_tag.extend([(t, 'matched_brand') for t in tokens if t in self.brand_list])
        #nlu_text_tag.extend([(t, 'matched_hotel') for t in tokens if t in self.hotel_list])
        
        nlu_text_tag.extend([(t,m) for m in self.mentioned_word_list  for t in tokens  if t.lower() == m.split('_')[1]])
        
        # NER
        for ent in nlu_processed_text.ents:
            entities.append((ent.text, ent.label_))
        
        nlu_text_tag.extend(entities)
        
        # intent classification
        intent = self.intentDetectionModel.predict([input_message])
        score = np.max(self.intentDetectionModel.predict_proba([input_message]))
        
        return tokens, intent, score, nlu_text_tag
    
    def date_converter(self, date_str):
        
        dateError = False
        fromdate = None # from date
        todate = None # to date
        now_delta = datetime.now() - self.datanow
        
        # dateparser cannot process leading word, need to be removed
        leading_word = ['previous','last', 'past']
        
        # datanow is not datetime.now, this reference date need to be ajusted accordingly 
        reference_date = ['months','mo','month','years','yr','year','d','day','quarter']
        
        # spacy does not split date period in between 'to'
        split_text_list = 'to'
        date_str1 = [s.split(split_text_list) if (split_text_list in s) else s for s in date_str ]
        
        # append splitted list from previous steps into single list without nested 
        date_str2 = list()
        for item in date_str1:
            if isinstance(item, list):
                for subi in item:
                    date_str2.append(subi)
            else:
                date_str2.append(item)
        
        # remove leading word
        date_str3 = list()
        for s in date_str2:
            for w in leading_word:
                if w in s:
                    s=s.replace(w, '').lstrip().rstrip()
            date_str3.append(s)
        
        # if reference date in the string
        found_reference_date = list()
        for d in date_str3:
            temp = list()
            for r in reference_date:
                temp.append(r in d.lower())
            found_reference_date.append(any(temp))
        
        for i in range(len(found_reference_date)):
            if found_reference_date[i] == True:
                if not re.match('\d+', date_str3[i]):
                    date_str3[i] = '1 ' + date_str3[i]
        
        # apply dateparser
        date_str4 = list()
        for d in date_str3:
            date_str4.append(dateparser.parse(d))
     
        # adjust now based on datanow
        for i in range(len(found_reference_date)):
            if found_reference_date[i] == True:
                if date_str4[i] is not None:
                    date_str4[i] = date_str4[i] - now_delta
                
        # remove none, not recognized by dateparser
        date_str4 = list(filter(None.__ne__, date_str4))
        
        # assuming time period only have max 2 date mentioned
        if (len(date_str4) > 2) and (len(date_str4) ==0):
            dateError = True
        
        # 2 date mentioned
        elif len(date_str4) == 2:
            todate, fromdate = max(date_str4), min(date_str4)
        
        # 1 date mentioned, assumed from date mentioned till 'now'
        elif len(date_str4) == 1:
            todate, fromdate = self.datanow, date_str4[0]
        
        return dateError, fromdate, todate
    
    def slot_filling(self, nlu_text_tag):
        '''
        to fill slots 
        '''
        print('Slots filling...')
        response = None
        for sl in self.intent['slot']:
            # already filled
            if sl['name'] in self.slots:
                continue
            
            self.s_counter += 1

            print(sl['name'])
            
            # to check if match possible value with user input tokenized text,
            slo = [(text, tag) for text, tag in nlu_text_tag if tag in sl['value_type']]
            
            # if slot if not found, check if default value available, if not check if mandatory
            # if fill, move substate to next slot
            if slo:
                if sl['name'] == 'period':
                    dateError, fromdate, todate = self.date_converter([date for date,tag in slo])
                    if not dateError:
                        self.slots[sl['name']] = [(fromdate, todate), 'DATE']
                    else:
                        response = 'Date period not recognized'
                        break
                else:        
                    self.slots[sl['name']] = slo
                self.s_counter = 0
            else:
                if sl['default']:
                    if sl['name'] == 'period':
                        self.slots[sl['name']] = [(self.datanow - timedelta(days=365), self.datanow), 'DATE']
                    else:
                        self.slots[sl['name']] =  [(sl['default'], sl['value_type'][0])]
                    
                    self.s_counter = 0
                    continue
                
                if sl['is_mandatory']:
                    response=sl['slot_filling_question']                          
                else: 
                    self.slots[sl['name']] = None
                    self.s_counter = 0
        
                    
        return response
    
    def slot_changing(self, nlu_text_tag):
        '''
        to handle slot changing for change intent
        '''
        slot_possible_tags_list = [sl['value_type'] for sl in self.intent['slot']]
        
        for text, tag in nlu_text_tag:
            
            findmatch = [tag in tags_list for tags_list in slot_possible_tags_list]
            
            if any(findmatch):
                matchslotname = list(compress(self.intent['slot'], findmatch))[0]['name']
                
                if self.slots[matchslotname] == text:
                    continue
                else:
                    self.slots[matchslotname] = [(text, tag)]
                    self.change_slot_request = 0
    
    def state_fulfillment_check(self):
        fulfilled = len(self.slots)
        required = len(self.intent['slot'])
        
        if fulfilled ==  required:
            self.state = 2

        elif self.s_counter > 0.3:
            self.state = 3
            
    def action_handler(self):
        print('perform action')
        aslots = self.slots
        fromdate = aslots['period'][0][0]
        todate = aslots['period'][0][1]
        
        database = self.database[(self.database['published_date'] > fromdate) & (self.database['published_date'] < todate)]

        if not (len(database) == 0):
            
            if (self.intent['name'] == 'list_top_entity') or self.intent['name'] == 'list_worst_entity':
                country,city,hotel= None, None,None
                filter_by_country,filter_by_city,filter_by_brand= None,None,None
                perf_metric = 'GRI'

                if aslots['entity1']:
                    if aslots['entity1'][0][1]=='matched_country': filter_by_country=aslots['entity1'][0][0]
                    if aslots['entity1'][0][1]=='matched_city': filter_by_city=aslots['entity1'][0][0] 
                    if aslots['entity1'][0][1]=='matched_brand': filter_by_brand=aslots['entity1'][0][0] 
                    
                if aslots['entity2']:
                    if aslots['entity2'][0][1]=="mentioned_country": country=True 
                    if aslots['entity2'][0][1]=="mentioned_city": city=True 
                    if aslots['entity2'][0][1]=='mentioned_hotel': hotel=True 
                
                if aslots['kpi']:
                    if aslots['kpi'][0][1]=='mentioned_gri': perf_metric=='GRI'
                    if aslots['kpi'][0][1]=='mentioned_sentiment': perf_metric='review_score'
                
                if self.intent['name'] == 'list_top_entity':
                    ascending_val = False
                    top_X = int(aslots['num_top'][0][0])
                else:
                    ascending_val = True
                    top_X = int(aslots['num_worst'][0][0])
                        
                response = performance_by(database,country=country,city=city,hotel=hotel, 
                                          perf_metric=perf_metric,top_X=top_X,
                                          filter_by_country=filter_by_country,filter_by_city=filter_by_city, filter_by_brand=filter_by_brand,
                                          ascending_val=ascending_val, debug=True)
                print(country,city,hotel,perf_metric,top_X,filter_by_country,filter_by_city,filter_by_brand,ascending_val)
            if (self.intent['name'] == 'list_good_aspect') or self.intent['name'] == 'list_bad_aspect':
                
                filter_by_hotel = aslots['entity_hotel'][0][0]
                ascending_val = False if self.intent['name'] == 'list_good_aspect' else True
    
                response = list_aspect(database,filter_by_hotel=filter_by_hotel, 
                                       top_X=5, ascending_val=ascending_val, debug=False)
                
            if self.intent['name'] == 'query_performance':
                filter_by_hotel = aslots['entity_hotel'][0][0]
                response = query_performance(database, filter_by_hotel=filter_by_hotel, perf_metric="GRI", top_X=1,
                                             ascending_val=False, debug=False )
        
        else: response="specified date period out of range"
   
        return response 
    
    def run(self,input_message): 
        
        # 0 to identify intent,1 to fill slots, 2 fulfilled, 3 error
        
        tokens, nlu_intent, nlu_score, nlu_text_tag = self.nlu(input_message)
        response = None
        
        print('1-nlu intent: %s, nlu_score: %.3f' % (nlu_intent[0], nlu_score))
        print('1-state: %d, i_counter: %d, s_counter: %d' % (self.state,self.i_counter,self.s_counter))
        print("1-suspected Intent: %s" % self.suspect_intent)
        
        if nlu_text_tag:
            for text, tag in nlu_text_tag:
                print("1-nlu_text_tag", text, tag)
                 
        # reset state if user did not ask for change 
        
        if (self.state == 2) and (nlu_intent != 'change'):
            self.state = 0
            self.i_counter=0            # to monitor error for intent identification
            self.s_counter=0            # to monitor error for slot filling 
            self.intent=None            # to store current intent 
            self.suspect_intent = None  # intent to be confirmed
            self.slots=dict()           # to store slots 
            self.change_slot_request=0  # flag for slot changing on-going
            
        # check if reset intent
        if (nlu_intent == 'reset') and (nlu_score > 0.7):
            self.state = 0
            self.i_counter=0            # to monitor error for intent identification
            self.s_counter=0            # to monitor error for slot filling 
            self.intent=None            # to store current intent 
            self.suspect_intent = None  # intent to be confirmed
            self.slots=dict()           # to store slots 
            self.change_slot_request=0  # flag for slot changing on-going
            response = 'Ok. Please ask a new question. eg. ... '
            
        else:
            
            if self.state == 0:
                
                if (nlu_intent == 'greeting') and (nlu_score > 0.7):
                    response = self.stand_ans['greeting']
                    
                # assign intent
                elif nlu_score > 0.7:
                    
                    self.state = 1
                    self.intent = [i for i in self.intents if i['name'] == nlu_intent][0]
                    response = self.slot_filling(nlu_text_tag)
                    
                    self.state_fulfillment_check()
                
                # intent not confirm
                elif nlu_score <= 0.7:
                    self.state = 3
                    self.i_counter += 1
                    
            elif self.state == 1:

                response = self.slot_filling(nlu_text_tag)
                self.state_fulfillment_check()

                # change slot request, original intent is save in self.intent
                # once slot change is fulfilled, change_slot_request = 0                    
            
            elif self.state == 2:
                if ((nlu_intent == 'change') and (nlu_score > 0.7)) or (self.change_slot_request == 1):
                    self.change_slot_request = 1
                    self.slot_changing(nlu_text_tag)
                    response = self.slot_filling(nlu_text_tag)
                    
                    self.state_fulfillment_check()
                    
        # if error state    
        if self.state == 3:
            
            print(self.i_counter)
            if (self.i_counter > 0) and (self.i_counter <= 3):
                if self.suspect_intent is None:
                    if nlu_score > 0.5:
                        self.suspect_intent = [i for i in self.intents if i['name'] == nlu_intent][0]['name']
                        self.suspect_intent_text_tag = nlu_text_tag
                        response = 'do you mean %s ?' % [i for i in self.intents if i['name'] == self.suspect_intent][0]['confirm_text']
                    else:
                        response = self.stand_ans['rephrase']
                elif (self.suspect_intent is not None) and ('yes' in tokens):
                    self.i_counter = 0
                    self.state = 1
                    self.intent = [i for i in self.intents if i['name'] == self.suspect_intent][0]
                    response = self.slot_filling(self.suspect_intent_text_tag)
                    self.suspected_intent = None
                    self.suspect_intent_text_tag = None
                    self.state_fulfillment_check()
                    
                else:
                    self.i_counter += 1
                    self.suspect_intent = None
                    self.suspect_intent_text_tag = None
                    response = self.stand_ans['rephrase']
                    
            elif self.i_counter > 3:
                response = self.stand_ans['error']
            
            if self.s_counter > 3:
                self.i_counter += 1
                response = self.stand_ans['error']
        
        # if all slots fulfilled
        if self.state == 2:
            response = self.action_handler()
        
        if (len(tokens) == 1) and (tokens[0] == 'HELP'):
            response = self.stand_ans['help']
        
        if (len(tokens) == 2) and (tokens[0] == 'REVIEW') and (tokens[1] == ':'):
            response = sentiment_pred(input_message, self.sent_tokenizer, self.sent_model)
        
        print('2-Intent detected : %s' % (self.intent['name'] if self.intent else 'None'))
        print("2-suspected Intent: %s" % self.suspect_intent)
        print("2-suspected intent text: %s" %self.suspect_intent_text_tag)
        print('2-state: %d, i_counter: %d, s_counter: %d' % (self.state,self.i_counter,self.s_counter))
        for key, item in self.slots.items():
            print('slots:', key, item )
            

        return response
    

                
                
                        
                


    
