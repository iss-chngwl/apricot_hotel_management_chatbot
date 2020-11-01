# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 14:02:50 2020

@author: chngweil
"""
#-------------------------------------------------------------------------------
import json 

intent_name = 'query_performance'
intent_confirm_text = 'to query the performance of a particular hotel?'
descriptions ='''
general query of information, can be gri, general sentiment score, or sentiment 
of an aspect for specific hotels at defined period (default period provided)
'''
reply=[]
slots=['kpi','entity_aspect','entity_hotel','period']
is_mandatory = [True, True, True, True]
slots_type = ['','', '', 'DATE']
defaults=['gri','overall','','-7'] # past 7 days

value_type =[['mentioned_gri','mentioned_sentiment'],
             ['mentioned_overall','mentioned_housekeeping','mentioned_location','mentioned_food'],
             ['matched_hotel_name'],
             ['DATE']
            ]
                 
slot_filling_question = ['Which performance do you like to review? GRI score or Customer review sentiment',
                         'I am now showing overall customer sentiment score. Which specific aspect would you like to review? housekeeping,location,food',
                         'Which hotel would you like to review the performance?',
                         'I am now showing last week performance, what time period are you looking at?']
                 
intent_query_performance = dict()
intent_query_performance['name'] = intent_name
intent_query_performance['confirm_text'] = intent_confirm_text
intent_query_performance['descriptions'] = descriptions
intent_query_performance['slot'] = []

for idx, item in enumerate(slots):
    intent_query_performance['slot'].append({
        'id': idx,
        'name': item,
        'default': defaults[idx],
        'slot_filling_question': slot_filling_question[idx],
        'value_type': value_type[idx],
        'is_mandatory': is_mandatory[idx]
        })
        


with open('intent_query_performance.json', 'w') as outfile:
    json.dump(intent_query_performance, outfile)

#--------------------------------------------------------------------------------------


intent_name = 'list_top_entity'
intent_confirm_text = 'to list some of the best performance hotel'
descriptions ='''
list top performance hotels/city/country at defined period(defaults: -7 days)
'''
reply=[]
slots=['entity1','entity2', 'num_top','period','kpi']
is_mandatory = [False, True, True, True, True]
hotel_hierarchy = ['mentioned_country','mentioned_city','mentioned_hotel']
defaults=['','',5,'-7','gri'] # past 7 days

value_type=[['matched_hotel','matched_city','matched_country'],
            ['mentioned_country','mentioned_city','mentioned_hotel'],
            ['CARDINAL'],
            ['DATE'],
            ['mentioned_gri','mentioned_sentiment']]
                 
slot_filling_question = ['',
                         'You want to review the best perform hotels? Cities? or Countries?',
                         '',
                         '',
                         '']

                 
intent_list_top_entity = dict()
intent_list_top_entity['name'] = intent_name
intent_list_top_entity['confirm_text'] = intent_confirm_text
intent_list_top_entity['descriptions'] = descriptions
intent_list_top_entity['slot'] = []

for idx, item in enumerate(slots):
    intent_list_top_entity['slot'].append({
        'id': idx,
        'name': item,
        'default': defaults[idx],
        'slot_filling_question': slot_filling_question[idx],
        'value_type': value_type[idx],
        'is_mandatory': is_mandatory[idx]
        })
        
with open('intent_list_top_entity.json', 'w') as outfile:
    json.dump(intent_list_top_entity, outfile)
#--------------------------------------------------------------------------------------


intent_name = 'list_worst_entity'
intent_confirm_text = 'to list some of the worst performance hotel'
descriptions ='''
list worst performance hotels/city/country at defined period(defaults: -7 days)
'''
reply=[]
slots=['entity_hi','entity_lo', 'num_worst','period']
is_mandatory = [False, True, True, True]
hotel_hierarchy = ['mentioned_country','mentioned_city','mentioned_hotel']
defaults=['','',5,'-7'] # past 7 days

value_type=[['matched_hotel','matched_city','matched_country'],
            ['mentioned_country','mentioned_city','mentioned_hotel'],
            ['CARDINAL'],
            ['DATE']
            ]

slot_filling_question = ['',
                         'You want to review the poor perform hotels? Cities? or Countries?',
                         '',
                         '']
                 
intent_list_worst_entity = dict()
intent_list_worst_entity['name'] = intent_name
intent_list_worst_entity['confirm_text'] = intent_confirm_text
intent_list_worst_entity['descriptions'] = descriptions
intent_list_worst_entity['slot'] = []

for idx, item in enumerate(slots):
    intent_list_worst_entity['slot'].append({
        'id': idx,
        'name': item,
        'default': defaults[idx],
        'slot_filling_question': slot_filling_question[idx],
        'value_type': value_type[idx],
        'is_mandatory': is_mandatory[idx]
        })

with open('intent_list_worst_entity.json', 'w') as outfile:
    json.dump(intent_list_worst_entity, outfile)


#--------------------------------------------------------------------------------------


intent_name = 'list_good_aspect'
intent_confirm_text = 'to list some of the good aspect of the hotel'
descriptions ='''
list good aspect for specific hotel at defined period(defaults: -7 days)
'''
reply=[]
slots=['entity_hotel','period']
is_mandatory = [True, True]
defaults=['','-7'] # past 7 days

value_type=[['matched_hotel'],['DATE']]
                 
slot_filling_question = ['Which hotel?',
                         'What time period you want to look at?']
                 
intent_list_good_aspect = dict()
intent_list_good_aspect['name'] = intent_name
intent_list_good_aspect['confirm_text'] = intent_confirm_text
intent_list_good_aspect['descriptions'] = descriptions
intent_list_good_aspect['slot'] = []

for idx, item in enumerate(slots):
    intent_list_good_aspect['slot'].append({
        'id': idx,
        'name': item,
        'default': defaults[idx],
        'slot_filling_question': slot_filling_question[idx],
        'value_type': value_type[idx],
        'is_mandatory': is_mandatory[idx]
        })

with open('intent_list_good_aspect.json', 'w') as outfile:
    json.dump(intent_list_good_aspect, outfile)
        
#--------------------------------------------------------------------------------------


intent_name = 'list_bad_aspect'
intent_confirm_text = 'to list some of the bad aspect of the hotel'
descriptions ='''
list bad aspect for specific hotel at defined period(defaults: -7 days)
'''
reply=[]
slots=['entity_hotel','period']
is_mandatory = [True, True]
hotel_hierarchy = ['mentioned_country','mentioned_city','mentioned_hotel']
defaults=['','-7'] # past 7 days

value_type=[['matched_hotel'],['DATE']]
                 
slot_filling_question = ['Which hotel?',
                         'What time period you want to look at?']
                 
intent_list_bad_aspect = dict()
intent_list_bad_aspect['name'] = intent_name
intent_list_bad_aspect['confirm_text'] = intent_confirm_text
intent_list_bad_aspect['descriptions'] = descriptions
intent_list_bad_aspect['slot'] = []

for idx, item in enumerate(slots):
    intent_list_bad_aspect['slot'].append({
        'id': idx,
        'name': item,
        'default': defaults[idx],
        'slot_filling_question': slot_filling_question[idx],
        'value_type': value_type[idx],
        'is_mandatory': is_mandatory[idx]
        })
    
with open('intent_list_bad_aspect.json', 'w') as outfile:
    json.dump(intent_list_bad_aspect, outfile)
            
    
#--------------------------------------------------------------------------------------


intent_name = 'change'
intent_confirm_text = 'to change your pervious query constraint'
descriptions ='''
change slot of other intents
'''
reply=[]
slots=['entity']
is_mandatory = [True]

defaults=[[]] # past 7 days

value_type=[[]]
                 
slot_filling_question = ['Which you want to look at?']
                 
intent_change = dict()
intent_change['name'] = intent_name
intent_change['confirm_text'] = intent_confirm_text
intent_change['descriptions'] = descriptions
intent_change['slot'] = []

for idx, item in enumerate(slots):
    intent_change['slot'].append({
        'id': idx,
        'name': item,
        'default': defaults[idx],
        'slot_filling_question': slot_filling_question[idx],
        'value_type': value_type[idx],
        'is_mandatory': is_mandatory[idx]
        })
     
with open('intent_change.json', 'w') as outfile:
    json.dump(intent_change, outfile)   
    
#--------------------------------------------------------------------------------------


intent_name = 'reset'
intent_confirm_text = 'to reset everything'
descriptions ='''
Reset everything, start again
'''
reply=[]
slots=[]
is_mandatory = []

defaults=[] # past 7 days

value_type=[]
                 
slot_filling_question = []
                 
intent_reset = dict()
intent_reset['name'] = intent_name
intent_reset['confirm_text'] = intent_confirm_text
intent_reset['descriptions'] = descriptions
intent_reset['slot'] = []

for idx, item in enumerate(slots):
    intent_reset['slot'].append({
        'id': idx,
        'name': item,
        'default': defaults[idx],
        'slot_filling_question': slot_filling_question[idx],
        'value_type': value_type[idx],
        'is_mandatory': is_mandatory[idx]
        })
    
with open('intent_reset.json', 'w') as outfile:
    json.dump(intent_reset, outfile)   
    
    
#--------------------------------------------------------------------------------------

intent_name = 'greeting'

descriptions ='''
greeting
'''
reply=['Hi, How are you? ... ']
slots=[]
is_mandatory = []

defaults=[] # past 7 days

value_type=[]
                 
slot_filling_question = []
                 
intent_greeting = dict()
intent_greeting['name'] = intent_name
intent_greeting['descriptions'] = descriptions
intent_greeting['slot'] = []

for idx, item in enumerate(slots):
    intent_greeting['slot'].append({
        'id': idx,
        'name': item,
        'default': defaults[idx],
        'slot_filling_question': slot_filling_question[idx],
        'value_type': value_type[idx],
        'is_mandatory': is_mandatory[idx]
        })

with open('intent_greeting.json', 'w') as outfile:
    json.dump(intent_greeting, outfile)   

    
#with open('intent_query_performance.json') as json_file:
#    data = json.load(json_file)
#
#-------------------------------------------------------------------
    
standard_answer = dict()  
standard_answer['name'] = 'general_answer'
standard_answer['description'] = '''
To define genearl asnwer to reponse to the user 
for greeeting, and help 
'''  
standard_answer['greeting'] = '''
Hey there!  
I am Jarvis, your hotel management chatbot, 
I can help you to review the hotel performance. 

You can ask question like:
- List top 5 best hotel in Singapore. 
- What people like about hotel X? 
- What is the customer senitment score about Hotel X housekeeping? 

You also can type: HELP if you need assistant. 

'''

standard_answer['help'] = '''
You can ask 
- List top 5 best hotel in Singapore. 
- What people like about hotel X? 
- What is the customer senitment score about Hotel X housekeeping? 

You can also type "reset" to start over again. 
'''
standard_answer['rephrase'] = '''
Sorry, I don't quite understand that
Can you rephrase your question? 
You can ask  
- List top 5 best hotel in Singapore. 
- What people like about hotel X? 
- What is the customer senitment score about Hotel X housekeeping? 
'''
standard_answer['error'] = '''
Sorry, I don't quite understand that. Try type: HELP for a list of recommended commands or type: Reset, to start all over
'''


with open('standard_answer.json', 'w') as outfile:
    json.dump(standard_answer, outfile)   