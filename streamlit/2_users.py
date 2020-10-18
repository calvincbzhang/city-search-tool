import streamlit as st

import numpy as np
import pandas as pd
import itertools
import random
from tqdm import tqdm
from geopy.distance import geodesic

import warnings
warnings.filterwarnings('ignore')

st.title("Users dataset definition")

cities_ds = pd.read_csv('../data/cities_ds.csv')

st.header("Functions")

st.subheader("Dataset generator")
with st.echo():
    def generate_dataset(multiplier = 5):
        # 0 is none, 1 is low, 2 is mid, 3 is high
        choices = [[0, 1, 2, 3]] * 6
        
        # create all possible combinations and repeat them to create bigger ds
        combinations = list(itertools.product(*choices)) * multiplier
        
        dataset = pd.DataFrame(columns=['Weights', 'City'])
        dataset['Weights'] = pd.Series(combinations)
        
        for index, row in tqdm(dataset.iterrows()):
            row['City'] = get_city(np.array(row['Weights']))
            
        return dataset

st.subheader("Random city choice")
with st.echo():
    def get_city(weights):
        # rank cities according to the weights given by the person
        ranked_cities = rank_cities(weights).reset_index(drop=True)
        
        # sample from uniform distribution and "randomly" select a city
        sample = np.random.uniform(0, 1, len(ranked_cities))
        prob_score = sample * list(ranked_cities['Score'])
        maximum = max(prob_score)
        if maximum != 0:
            chosen = [int(i/maximum) for i in prob_score]
        else:
            chosen = [0] * len(ranked_cities)
            chosen[random.randint(0, len(chosen))] = 1
            
        ranked_cities['Chosen'] = pd.Series(chosen)
            
        return ranked_cities[ranked_cities['Chosen'] == 1]['City'].values[0]

st.subheader("Cities personal ranking")
with st.echo():
    def rank_cities(weights):
        features = ['Purchase Power', 'Health Care', 'Pollution', 'QoL_H', 'Crime Rating', 'Unesco']
        
        # pollution and crime rating have a negative impact, whist the other features have a positive one
        weights *= [2, 2, -2, 2, -2, 1]
        
        norm = lambda xs: (xs-xs.min())/(xs.max()-xs.min())
        # e^(2x) to increase the probability of getting the most compatible city
        cities_ds['Score'] = np.exp(norm(cities_ds[features].dot(weights)) * 10)
        
        return cities_ds.sort_values('Score', ascending=False).fillna(0)

people = generate_dataset(5)

st.header("Final dataset")
st.write(people.head())