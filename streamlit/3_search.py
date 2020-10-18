# imports
import streamlit as st
import pandas as pd
import numpy as np
import itertools
import random
import io
import requests

from sklearn.manifold import TSNE
#%matplotlib inline
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

import warnings
warnings.filterwarnings('ignore')

st.title("City Search Tool")

cities_ds=pd.read_csv('../data/cities_ds.csv')
people_ds = pd.read_csv('../data/people_ds_100.csv')
people= people_ds['Weights'].str.replace('(', '', regex=True).str.replace(')', '', regex=True).str.replace(',', '', regex=True).str.split(expand=True)

from sklearn.metrics.pairwise import manhattan_distances, euclidean_distances

st.header("Choose your priorities")
options = ["None", "Low", "Mid", "High"]
weights = ["None", "None", "None", "None", "None", "None"]

weights[0] = st.selectbox('Purchase Power', options)
weights[1] = st.selectbox('Health Care', options)
weights[2] = st.selectbox('Pollution', options)
weights[3] = st.selectbox('Quality of Life', options)
weights[4] = st.selectbox('Crime Rating', options)
weights[5] = st.selectbox('Unesco Sites', options)

replace = {'None': 0, 'Low': 1, 'Mid': 2, 'High': 3}
weights = np.array([replace[x] for x in weights])

df = pd.DataFrame(weights).T

people_ds['md'] = pd.DataFrame(manhattan_distances(df, people)).T
topk_people = pd.DataFrame(people_ds.sort_values('md').head(20)['City'].unique(),columns={'City'})
topk_people_city = pd.merge(topk_people['City'], cities_ds[['City','Purchase Power', 'Health Care', 'Pollution', 'QoL_H', 'Crime Rating', 'Unesco']], on='City')

topk_city = pd.DataFrame(euclidean_distances(topk_people_city[['Purchase Power', 'Health Care', 'Pollution', 'QoL_H', 'Crime Rating', 'Unesco']],
                                             cities_ds[['Purchase Power', 'Health Care', 'Pollution', 'QoL_H', 'Crime Rating', 'Unesco']])).T
topk_city['mean'] = topk_city.mean(axis=1)

city_Score = pd.concat([cities_ds['City'], topk_city['mean']], axis=1)


st.header("Result")
st.write(city_Score.sort_values('mean')["City"][:10].reset_index(drop=True).head(10))