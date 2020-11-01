#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 22:19:58 2020

@author: jiahao
"""

import pandas as pd
import re

# import data
df_2018 = pd.read_excel(r'/Users/jiahao/Google Drive/ISS/EBA5004/PLP Project/Data/2018 All Reviews.xlsx',
                       skiprows = range(0, 7))
df_2019 = pd.read_excel(r'/Users/jiahao/Google Drive/ISS/EBA5004/PLP Project/Data/2019 All Reviews.xlsx',
                       skiprows = range(0, 7))
df_2020 = pd.read_excel(r'/Users/jiahao/Google Drive/ISS/EBA5004/PLP Project/Data/2020 All Reviews.xlsx',
                       skiprows = range(0, 7))

df = pd.concat([df_2018, df_2019, df_2020])

df = df[["Language", "Hotel Name", "GRI™", "Published Date", "Review Score", "Classification", "Review Text"]]

# extract english data (based on the column "Language")
df = df[df.Language.isin(['en'])]

df.dropna(inplace=True)

df['Review Text Original'] = df['Review Text']
df['Review Text'] = df['Review Text Original'].map(lambda x: re.sub(r'[^\x00-\x7f]',r'', x))
df['Word Count'] = df['Review Text'].apply(lambda x: len(str(x).split()))
df = df[df['Word Count'] > 4]  

df.drop(['Language', 'Word Count'], axis=1, inplace=True)
df.reset_index(drop=True ,inplace=True)



#%% join data
df_mapping = pd.read_excel(r'/Users/jiahao/Google Drive/ISS/EBA5004/PLP Project/Data/Property Mapping.xlsx')
df_joined = pd.merge(df, df_mapping.rename({'Property Name': 'Hotel Name'}, axis=1), how='left', on='Hotel Name', indicator=True)

# check joined data
# df_joined[df_joined["_merge"]!='both']["Hotel Name"].value_counts()
# df_mapping[df_mapping["Property Name"]=="Somerset on The Pier Hobart"]["Property Name"].value_counts()

df = df_joined[df_joined["_merge"]=='both']
df.drop(['_merge'], axis=1, inplace=True)
df.reset_index(drop=True ,inplace=True)

df.rename(
    columns={"Hotel Name": "full_hotel_name",
             "GRI™": "GRI",
             "Published Date": "published_date",
             "Review Score": "review_score",
             "Classification": "classification",
             "Review Text": "review_text",
             "Review Text Original": "review_text_original",
             "Country": "hotel_country_name",
             "City": "hotel_city_name",
             "Brand": "hotel_brand_name"},
    inplace = True
    )

df['GRI'] = df['GRI'].str.rstrip('%').astype('float') / 100.0
df['review_score'] = df['review_score'].str.rstrip('%').astype('float') / 100.0

df.to_excel('full_reviews.xlsx', encoding='utf-8', index=False)