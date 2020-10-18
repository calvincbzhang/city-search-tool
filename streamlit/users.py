import streamlit as st

import numpy as np
import pandas as pd
import itertools
import random
from tqdm import tqdm
from geopy.distance import geodesic


def users():
    st.title("Users dataset")