#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 02:48:55 2023

@author: somshubhrodatta
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

# Load your data
weather = pd.read_csv('IndianWeatherRepository.csv')
rain = pd.read_csv('district wise rainfall normal.csv')
recomm = pd.read_csv('crop_recommendation.csv')
soil = pd.read_csv('soil.csv')
sr=pd.read_csv('sr.csv')
sr=sr[['Soil_type','Crop']]
# Preprocess the data
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
    'South Twenty Four Parganas': 'Sounth 24 Parganas',
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
weather['location_name'] = weather['location_name'].str.upper()
weather['region'] = weather['region'].str.upper()
recomm['label'] = recomm['label'].str.lower()
soil['State'] = soil['State'].str.upper()
soil['Soil_type']=soil['Soil_type'].str.lower()
sr['Crop']=sr['Crop'].str.lower()
sr['Soil_type']=sr['Soil_type'].str.lower()

# Merge weather and rain DataFrames based on matching columns
climate = pd.merge(weather, rain, left_on=['region', 'location_name'], right_on=['STATE_UT_NAME', 'DISTRICT'])

# Select features and target
features = ['temperature_celsius', 'humidity', 'JUL', 'Soil_type']
target = 'label'
df = pd.merge(climate, soil, left_on='STATE_UT_NAME', right_on='State')
df1 = pd.merge(sr, recomm, left_on='Crop', right_on='label')
df1.to_csv('ss.csv')
label_mapping = {label: idx for idx, label in enumerate(df1['label'].unique())}
print(df['DISTRICT'].unique())
df1['label_encoded'] = df1['label'].map(label_mapping)
df['label']=''
# Preprocess categorical features
le_soil = LabelEncoder()
le_crop = LabelEncoder()
df1['Soil_type'] = le_soil.fit_transform(df1['Soil_type'])
df1['label'] = le_crop.fit_transform(df1['label'])
# Select features and target
X = df1[['temperature', 'humidity', 'rainfall','Soil_type']]
y = df1['label']
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.001, random_state=42)
'''X_train=df1[['temperature', 'humidity', 'rainfall', 'Soil_type']]
y_train=df1['label']
X_test=df[['temperature_celsius', 'humidity', 'JUL', 'Soil_type']]
y_test=df['label']'''
# Train a decision tree classifier
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Get user input for district, temperature, humidity, and rainfall
district = input("Enter the district: ").upper()
print()
temperature = df[df['DISTRICT'] == district]['temperature_celsius'].values[0]
humidity = df[df['DISTRICT'] == district]['humidity'].values[0]
rainfall = df[df['DISTRICT'] == district]['AUG'].values[0]
soil_type_str = df[df['DISTRICT'] == district]['Soil_type'].values[0]

# Use the LabelEncoder to convert string to numerical representation
soil_type_encoded = le_soil.transform([soil_type_str])[0]

input_data = [[temperature, humidity, rainfall,soil_type_encoded]]
predicted_label = model.predict(input_data)[0]
'''print("label_mapping:", label_mapping)
print("predicted_label:", predicted_label)'''

recommended_crop = [label for label, idx in label_mapping.items()if idx == predicted_label]

# Reverse transform the label to get the crop name
#recommended_crop = le_crop.inverse_transform([predicted_label])

print(f'Recommended crop for {district.title()}: {recommended_crop[0]}')
print("Soil:",df[df['DISTRICT'] == district]['Soil_type'].values[0])
print("Annual Rainfall(cm):",df[df['DISTRICT'] == district]['ANNUAL'].values[0])
print("Temperature(C):",df[df['DISTRICT'] == district]['temperature_celsius'].values[0])
print("Humidity:",df[df['DISTRICT'] == district]['humidity'].values[0],"\n\n")
