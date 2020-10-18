import streamlit as st

import numpy as np
import pandas as pd
import itertools
import random
from tqdm import tqdm
from geopy.distance import geodesic

from preproc import preprocessing
from users import users

import warnings
warnings.filterwarnings('ignore')


pages = {'preprocessing':preprocessing,'users': users}

choice = st.sidebar.radio("Choice your page: ",tuple(pages.keys()))

pages[choice]()

