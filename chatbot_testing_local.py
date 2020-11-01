# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 10:21:38 2020

@author: chngweil
"""
import pandas as pd
#database = pd.read_csv("./Data/demo_reviews (edited cols).csv", header=0, index_col=0)
#database['published_date'] = pd.to_datetime(database['published_date'])

jarv = agent_jarvis2()

#greeting
user_input = 'Hi!'

# list top 
user_input = 'list top 5 hotel in Singapore by sentiment'
user_input = 'list top 5 hotel in Thailand by GRI'

# list aspect
user_input = 'what people like about Somerset Maison Asoke?'
user_input = 'yes'

# Slot filling question
user_input = 'list top 10'
user_input = 'hotel'

# question to for confirmation
user_input ='Can you show me top hotel in Vietnam starting from February'
user_input ='yes'

# question to change slot
user_input = 'list top  hotel in Singapore from January 2019'
user_input = 'forget about Singapore, i want to check Malaysia'

# Reset
user_input = 'reset, start over again'

# help
user_input = 'HELP'

response = jarv.run(user_input)
print("response : %s" %response)


'''
dialogue state tracking adopted Handcrafted approach, required to simulate 
 all possible scenario that how user may ask the question, in order to determine the dialogue state
 The chatbot may fail, if there is scenario not aware in the development phase

date parsing method are not perfect, sometime may not get the correct meaning from the 
 natural language, for example, list best hotel in Singapore from in year 2019
 The date parser method is not able to define the date as January 2019 to December 2019 
 more specific way of mentioning required in the text itself
 
review database is not updated timely, chatbot can only review the historical static database 


''' 