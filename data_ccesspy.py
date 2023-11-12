#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 18:07:09 2023

@author: somshubhrodatta
"""

import pandas as pd
import geopandas as gpd
import numpy as np

# Load your data
agri = pd.read_csv('Agri_district.csv')
weather = pd.read_csv('IndianWeatherRepository.csv')
rain = pd.read_csv('district wise rainfall normal.csv')
recomm = pd.read_csv('crop_recommendation.csv')
soil = pd.read_csv('soil.csv')
geo = gpd.read_file(filename='india_geo')
sr=pd.read_csv('soil_recomm.csv')
soil_crops_mapping = {
    'red and yellow': ['rice', 'maize', 'chickpea', 'kidneybeans', 'pigeonpeas', 'mothbeans', 'mungbean', 'blackgram', 'lentil', 'pomegranate', 'banana', 'mango', 'grapes', 'watermelon', 'muskmelon', 'apple', 'orange', 'papaya', 'coconut', 'cotton', 'jute', 'coffee'],
    'alluvial': ['rice', 'maize', 'chickpea', 'kidneybeans', 'pigeonpeas', 'mothbeans', 'mungbean', 'blackgram', 'lentil', 'pomegranate', 'banana', 'mango', 'grapes', 'watermelon', 'muskmelon', 'apple', 'orange', 'papaya', 'coconut', 'cotton', 'jute', 'coffee'],
    'black': ['rice', 'maize', 'chickpea', 'kidneybeans', 'pigeonpeas', 'mothbeans', 'mungbean', 'blackgram', 'lentil', 'pomegranate', 'banana', 'mango', 'grapes', 'watermelon', 'muskmelon', 'apple', 'orange', 'papaya', 'coconut', 'cotton', 'jute', 'coffee'],
    'laterite': ['cashew', 'rubber', 'coconut'],
    'desert': ['pearl millet', 'mustard', 'bajra'],
    'mountain': ['potatoes', 'apples', 'tea'],
    'red': ['groundnuts', 'pulses', 'jute']
}

# Select the columns you need
agri = agri[['state', 'district', 'market', 'commodity', 'modal_price']]
weather = weather[['region', 'location_name', 'temperature_celsius', 'humidity']]
rain = rain[['STATE_UT_NAME', 'DISTRICT', 'ANNUAL']]
recomm = recomm[['temperature', 'humidity', 'rainfall', 'label']]
weather['region']=weather['region'].str.upper()

district_replacements = {
    'Thrissur': 'Thirssur',
    'Viluppuram': 'Villupuram',
    'Kasaragod': 'Kasargod',
    'Vadodara': 'Vadodara(Baroda)',
    'Bulandshahr': 'Bulandshahar',
    'Tarn Taran': 'Tarntaran',
    'Sundargarh': 'Sundergarh',
    'Kannauj': 'Kannuj',
    'Dehradun': 'Dehradoon',
    'Jalor': 'Jalore',
    'Sipahijula': 'Sepahijala',
    'South Twenty Four Parganas': 'South 24 Parganas',
    'Solapur': 'Sholapur',
    'Moradabad': 'Muradabad',
    'Rupnagar': 'Ropar (Rupnagar)',
    'North Twenty Four Parganas': 'North 24 Parganas',
    'Lakhimpur': 'Khiri (Lakhimpur)',
    'Panch Mahals': 'Panchmahals',
    'Maldah': 'Malda',
    'Barddhaman':'Burdwan',
    'Barwani': 'Badwani',
    'Paschim Medinipur': 'Medinipur(W)',
    'Gautam Buddha Nagar': 'Gautam Budh Nagar',
    'Chitrakoot': 'Chitrakut',
    'Rangareddy': 'Ranga Reddy',
    'Narsimhapur': 'Narsinghpur',
    'Chittoor': 'Chittor',
    'Anugul': 'Angul',
    'Farrukhabad': 'Farukhabad',
    'Nabarangapur': 'Nowarangpur',
    'Tiruvannamalai': 'Thiruvannamalai',
    'Jalaun': 'Jalaun (Orai)',
    'Bathinda': 'Bhatinda',
    'Hugli': 'Hooghly',
    'Hydrabad': 'Hyderabad',
    'Ahmadnagar': 'Ahmednagar',
    'Rae Bareli': 'Raebarelli',
    'Udham Singh Nagar': 'UdhamSinghNagar',
    'Kanniyakumari': 'Nagercoil (Kannyiakumari)',
    'Anuppur': 'Anupur',
    'Chittaurgarh': 'Chittorgarh',
    'Buldana': 'Buldhana'
}
for (o, r) in district_replacements.items():
    weather['location_name'].replace(to_replace=o, value=r, inplace=True)
print(recomm['label'].unique())   
soil['State']=soil['State'].str.upper()    
weather['location_name']=weather['location_name'].str.upper()
weather['region']=weather['region'].str.upper()
# Merge weather and rain DataFrames based on matching columns
climate = pd.merge(weather, rain, left_on=['region', 'location_name'], right_on=['STATE_UT_NAME', 'DISTRICT'])
recomm=pd.merge(recomm, sr, left_on='label', right_on='Crops')
rc = {}

'''d = input("District: ")
t,r,h,s='','','',''
for i1, r1 in climate.iterrows():
    if r1['DISTRICT'] == d.upper():
        t,r,h=r1['temperature_celsius'], r1['ANNUAL'],r1['humidity']
        for i2, r2 in recomm.iterrows():  # Use recomm.iterrows() for proper iteration
            c = 0
            if abs(r1['temperature_celsius'] - r2['temperature'])==0:
                c+=1
                c += 1
            if abs(r1['ANNUAL'] - r2['rainfall'])<=0:
                c += 1
            if abs(r1['humidity'] - r2['humidity'])==0:
                c += 1
            for i3,r3 in soil.iterrows():
                if r3['State']==r1['STATE_UT_NAME']:
                    s= r3['Soil_type']
                    if r2['label'] in soil_crops_mapping[r3['Soil_type'].lower()]:
                        rc[r2['label']] = c
print("Soil Type: ", s,"\nTemp(C): ", t, "\nAnnual rainfall(cm): ", r, "\nHumidity: ", h)
print("Recommended crops: ")
rc = {k: v for k, v in sorted(rc.items(), key=lambda item: item[1],reverse=True)}
c=0
for i in rc.keys():
    if c<3:
        if rc[i] >= 2:
            print(i)
            c+=1'''


'''d=input("District: ")
t,c=0,0
for index,row in agri.iterrows():
    if row['district']==d:
        t+=row['modal_price']
        c+=1
if c!=0:
    t/=c
print("Avg modal price in {} is ".format(d),t)'''