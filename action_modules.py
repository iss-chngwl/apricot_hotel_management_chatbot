# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 10:11:00 2020

@author: chngweil
"""

import pandas as pd

def pprint_dataframe_output(output_df, top_X):
    return ", ".join([k+": "+str(round(v, 3)) for k,v in output_df[0:top_X].values.tolist()])


def performance_by(database, country=None, city=None, hotel=None, perf_metric="GRI", top_X=5, 
                   filter_by_country=None, filter_by_city=None, filter_by_brand=None,
                  ascending_val=False, debug=False):

    filter_name, filter_field, filter_item, groupby_name, groupby_field = None, None, None, None, None
    top_bottom = "bottom" if ascending_val else "top"
    if filter_by_brand!=None and hotel:
        #filter by brand, groupby hotel, sort by top_X, perf_metric
        filter_name, filter_field, filter_item = "brand", "hotel_brand_name", filter_by_brand
        groupby_name, groupby_field = "hotels", "full_hotel_name"
        if debug: print("filter by city, groupby hotel")
    elif filter_by_city!=None and hotel:
        #filter by city, groupby hotel, sort by top_X, perf_metric
        filter_name, filter_field, filter_item = "city", "hotel_city_name", filter_by_city
        groupby_name, groupby_field = "hotels", "full_hotel_name"
        if debug: print("filter by city, groupby hotel")
    elif filter_by_country!=None and hotel:
        #filter by country, groupby hotel, sort by top_X, perf_metric
        filter_name, filter_field, filter_item = "country", "hotel_country_name", filter_by_country
        groupby_name, groupby_field = "hotels", "full_hotel_name"
        if debug: print("filter by country, groupby hotel")
    elif filter_by_country!=None and city:
        #filter by country, groupby city, sort by top_X, perf_metric
        filter_name, filter_field, filter_item = "country", "hotel_country_name", filter_by_country
        groupby_name, groupby_field = "cities", "hotel_city_name"
        if debug: print("filter by city, groupby hotel")
    elif hotel:
        #groupby hotel, sort by top_X, perf_metric
        filter_name, filter_field, filter_item = None, None, None
        groupby_name, groupby_field = "hotels", "full_hotel_name"
        if debug: print("groupby hotel")
    elif city:
        #groupby city, sort by top_X, perf_metric
        filter_name, filter_field, filter_item = None, None, None
        groupby_name, groupby_field = "cities", "hotel_city_name"
        if debug: print("groupby city")
    elif country:
        #groupby country, sort by top_X, perf_metric
        filter_name, filter_field, filter_item = None, None, None
        groupby_name, groupby_field = "countries", "hotel_country_name"
        if debug: print("groupby country")  
    else:
        return "Unable to answer, error"
    try:
        if filter_field != None:
            if debug: print("filter col is %s, item is %s" %(filter_field, filter_item))
            filtered_df = database[database[filter_field] == filter_item]
            output_df = filtered_df.groupby(groupby_field).agg({perf_metric:"mean"}).reset_index().sort_values(perf_metric, ascending=ascending_val)
            return "The %s %s %s in %s are %s by %s" %(top_bottom, top_X, groupby_name, filter_item, pprint_dataframe_output(output_df, top_X), perf_metric)
        else:
            output_df = database.groupby(groupby_field).agg({perf_metric:"mean"}).reset_index().sort_values(perf_metric, ascending=ascending_val)
            return "The %s %s %s are %s by %s" %(top_bottom, top_X, groupby_name, pprint_dataframe_output(output_df, top_X), perf_metric)
    except:
        return "The %s %s is not in our dataset" %(filter_name, filter_item)
    
    
def list_aspect(database, filter_by_hotel=None, top_X=5, ascending_val=False, debug=False):
    
    aspect_scores = [x for x in database.columns.tolist() if "aspect" in x]
    #aspect_scores = ["aspect_food_score", "aspect_location_score", "aspect_service_score"]
    filter_name, filter_field, filter_item = "hotel", "full_hotel_name", filter_by_hotel
    best_worst = "worst" if ascending_val else "best"

    try:
        if filter_by_hotel != None:
            if debug: print("filter col is %s, item is %s" %(filter_field, filter_item))
            filtered_df = database[database[filter_field] == filter_item]
            output_df = filtered_df.groupby(filter_field)[aspect_scores].agg(["mean"]).reset_index()
            output_df.columns = output_df.columns.get_level_values(0)
            sorted_aspect_df = output_df[aspect_scores].melt().sort_values(by="value", ascending=ascending_val)
            aspect = sorted_aspect_df["variable"].values[0].split("_")[1]
            
            return "The %s aspect of %s is %s. \n%s" %(best_worst, filter_item, aspect, pprint_dataframe_output(sorted_aspect_df, top_X))
    except:
        return "The %s %s is not in our dataset" %(filter_name, filter_item)    
    
    
    
def query_performance(database, filter_by_hotel=None, perf_metric="GRI", top_X=1,
                      ascending_val=False, debug=False ):
    
    filter_name, filter_field, filter_item = "hotel", "full_hotel_name", filter_by_hotel
    best_worst = "worst" if ascending_val else "best"

    try:
        if filter_by_hotel != None:
            if debug: print("filter col is %s, item is %s" %(filter_field, filter_item))
            filtered_df = database[database[filter_field] == filter_item]
            output_df = filtered_df.groupby(filter_field).agg({perf_metric:"mean"}).reset_index().sort_values(perf_metric, ascending=ascending_val)
            return "For %s, %s" %(perf_metric, pprint_dataframe_output(output_df, top_X))
    except:
        return "The %s %s is not in our dataset" %(filter_name, filter_item)    