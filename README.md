# Apricot_hotel_management_chatbot

This project aims to buil a chatbot system for hotel management to assist management to quickly understand the property performances and respond to customer feedback. 

The chatbot system consists of the following functions:
* Understand and extract key information from user input questions
* Provide and overall sentiment class based on customer reviews
* Provide sentiment and polarity scores for various aspects at hotel, city, country or brand level
* Provide list of top popular hotels based on different specifide KPI


## Prerequisites

* check out requirement.txt for required python packages
* Additinally, Installation of spaCY and the required models:
```
    	pip install -U spacy
    	python -m spacy download en_core_web_sm
```
* Integration of chatbot into Slack [Slack bot Setup](https://medium.com/nerd-for-tech/how-to-make-a-slack-bot-in-python-using-slacks-rtm-api-335b393563cd) 

## Running the tests

Once the Slack channel and bot is setup, remember to obtain the Slack token
```
python chatbot_tesing_slack.py
```
