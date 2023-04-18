"""
Miguel Candido Aurora Peralta
ISTA 350 Final Project Spring 2023

Generates three visualizations regarding generation of electricity using data
obtained from the US Energy Information Administration API.
"""

import requests
import pandas as pd
import json

"""
SECTION 1: Methods retrieving data from EIA API
URLS obtained from the API query browser at
https://www.eia.gov/opendata/browser and further modified to include key and
specify json output type.
"""

def get_general_netgen_data(key):
    """
    Given an EIA API key, returns a dataframe. Dataframe contains the net
    generation of electricity separated by generation method (solar, wind,
    etc). Numbers cover all sectors and parts of the US. 
    """

    url = f"https://api.eia.gov/v2/electricity/electric-power-operational-data/data/?api_key={key}&frequency=monthly&data[0]=generation&facets[fueltypeid][]=AOR&facets[location][]=US&facets[sectorid][]=99&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000&out=json"
    pass

def get_netgen_by_sector(key):
    """
    Given an EIA API key, returns a dataframe. Dataframe contains the net
    generation of electricity separated by generation method (solar, wind,
    etc.) and sector (industrial, commercial, residential).
    """
    pass

def get_netgen_by_state(key):
    """
    Given an EIA API key, returns a dataframe. Dataframe contains the net
    generation of electricity separated by generation method (solar, wind, etc.) and US state.
    """
    pass

"""
SECTION 2: Processing dataframes from API queries into what is needed for
visualizations. 
"""

def general_netgen_df(df):
    pass

def netgen_by_sector_df(df):
    pass

def netgen_by_state_df(df):
    pass

"""
SECTION 3: Generating visualizations using matplotlib
"""

def general_netgen_viz(df):
    pass

def netgen_by_sector_viz(df):
    pass

def netgen_by_state_viz(df):
    pass