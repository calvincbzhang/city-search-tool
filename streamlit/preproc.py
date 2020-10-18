import streamlit as st

import numpy as np
import pandas as pd
import itertools
import random
from tqdm import tqdm
from geopy.distance import geodesic


def preprocessing():
    st.title('Data pre-processing')

    #Datasets
    st.header("Initial datasets")

    MHQoL = pd.read_csv('../data/movehubqualityoflife.csv')
    cities = pd.read_csv('../data/cities.csv')
    HappinessIndex = pd.read_csv('../data/2019.csv')
    UnescoSites = pd.read_csv('../data/whc-sites-2019.csv')

    st.subheader("MoveHub City Ratings - Quality of life")
    st.write(MHQoL.head())
    st.text("")

    st.subheader("Cities - Countries")
    st.write(cities.head())
    st.text("")

    st.subheader("World Happiness Index")
    st.write(HappinessIndex.head())
    st.text("")

    st.subheader("Unesco Sites")
    st.write(UnescoSites.head())
    st.text("")


    #City-Country / Happiness / Unesco
    st.header("Country and Happiness")

    with st.echo():
        City_Country = pd.merge(MHQoL[['City','Purchase Power', 'Health Care', 'Pollution', 'Quality of Life', 'Crime Rating','lat','lng']], cities, on='City')

        HappinessIndex = HappinessIndex.rename(columns={'Country or region': 'Country', 'Score': 'Happiness_Score'})

        City_Country_Happiness = pd.merge(City_Country, HappinessIndex[['Country','Happiness_Score']], on='Country')

        def get_unesco(city):
            distances = UnescoSites.apply(lambda sites : geodesic((sites['latitude'],sites['longitude']), (city['lat'], city['lng'])).kilometers,1)
            return sum(map(lambda x : x<100, distances))

        City_Country_Happiness['Unesco'] = City_Country_Happiness.apply(get_unesco, 1)

    st.write(City_Country_Happiness.head())

    #Normalization and reorder
    st.header("Final modifications")

    st.subheader("Normalization")
    with st.echo():
        features = ['Purchase Power', 'Health Care', 'Quality of Life', 'Pollution', 'Crime Rating', 'Happiness_Score', 'Unesco']

        norm = lambda xs: (xs-xs.min())/(xs.max()-xs.min())
        City_Country_Happiness[features] = (norm(City_Country_Happiness[features]) * 100)

        City_Country_Happiness['QoL_H'] = (City_Country_Happiness['Quality of Life'] + City_Country_Happiness['Happiness_Score']) / 2

    # reorder columns
    cities_ds = City_Country_Happiness[['City', 'Country', 'Purchase Power', 'Health Care', 'Pollution', 'QoL_H', 'Crime Rating', 'Unesco']]

    st.write(cities_ds.head())
