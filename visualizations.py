"""
Miguel Candido Aurora Peralta
ISTA 350 Final Project Spring 2023

Generates three visualizations regarding generation of electricity using data
obtained from the US Energy Information Administration API.
"""

import requests
import pandas as pd
import json

#SECTION 1: Methods retrieving data from EIA API
"""
URLS obtained from the API query browser at
https://www.eia.gov/opendata/browser and further modified to include key and
specify json output type.

Energy sources to be included:
    BIO - biomass
    COW - all coal products
    GEO - geothermal
    HYC - conventional hydroelectric
    NG - natural gas
    NUC - nuclear
    PC - petroleum coke
    PEL - petroleum liquids
    SUN - solar
    WND - wind

I chose to include the sources of energy discussed in the EIA's article about
energy sources here:
https://www.eia.gov/energyexplained/what-is-energy/sources-of-energy.php
Note: Hydrocarbon gas liquids are in this article but were not listed as an
option in the API, I'm assuming they're included in the natural gas and
petroleum numbers as they're produced during oil and natural gas extraction.
"""

def get_general_netgen_data(key):
    """
    Given an EIA API key, returns a dataframe. Dataframe contains the net
    generation of electricity separated by generation method (solar, wind,
    etc). Numbers cover all sectors and parts of the US. 
    """
    
    url = f"https://api.eia.gov/v2/electricity/electric-power-operational-data/data/?api_key={key}&frequency=annual&data[0]=generation&facets[fueltypeid][]=BIO&facets[fueltypeid][]=COW&facets[fueltypeid][]=GEO&facets[fueltypeid][]=HYC&facets[fueltypeid][]=NG&facets[fueltypeid][]=NUC&facets[fueltypeid][]=PC&facets[fueltypeid][]=PEL&facets[fueltypeid][]=SUN&facets[fueltypeid][]=WND&facets[location][]=US&facets[sectorid][]=99&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000&out=json"
    response = requests.get(url).json()
    
    # dict of data is inside of another nested list 'response'
    data = response['response']['data']
    df = pd.DataFrame.from_records(data)
    return df

def get_netgen_by_sector(key):
    """
    Given an EIA API key, returns a dataframe. Dataframe contains the net
    generation of electricity separated by generation method (solar, wind,
    etc.) and sector (industrial, commercial, residential) for only 2022.
    
    sectorid:
    1 - electric utility
    94 - independent power producers
    96 - all commercial
    97 - all industrial
    """

    url = f"https://api.eia.gov/v2/electricity/electric-power-operational-data/data/?api_key={key}&frequency=annual&data[0]=generation&start=2021&end=2022&facets[fueltypeid][]=BIO&facets[fueltypeid][]=COW&facets[fueltypeid][]=GEO&facets[fueltypeid][]=HYC&facets[fueltypeid][]=NG&facets[fueltypeid][]=NUC&facets[fueltypeid][]=PC&facets[fueltypeid][]=PEL&facets[fueltypeid][]=SUN&facets[fueltypeid][]=WND&facets[location][]=US&&facets[sectorid][]=1&facets[sectorid][]=94&facets[sectorid][]=96&facets[sectorid][]=97&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000&out=json"
    response = requests.get(url).json()

    # dict of data is inside of another nested list 'response'
    data = response['response']['data']
    df = pd.DataFrame.from_records(data)
    return df

def get_netgen_by_state(key):
    """
    Given an EIA API key, returns a dataframe. Dataframe contains the net
    generation of electricity separated by generation method (solar, wind,
    etc.), and US state + District of Columbia.
    """
    url = f"https://api.eia.gov/v2/electricity/electric-power-operational-data/data/?api_key={key}&frequency=annual&data[0]=generation&start=2021&end=2022&facets[fueltypeid][]=BIO&facets[fueltypeid][]=COW&facets[fueltypeid][]=GEO&facets[fueltypeid][]=HYC&facets[fueltypeid][]=NG&facets[fueltypeid][]=NUC&facets[fueltypeid][]=PC&facets[fueltypeid][]=PEL&facets[fueltypeid][]=SUN&facets[fueltypeid][]=WND&facets[location][]=AK&facets[location][]=AL&facets[location][]=AR&facets[location][]=AZ&facets[location][]=CA&facets[location][]=CO&facets[location][]=CT&facets[location][]=DC&facets[location][]=DE&facets[location][]=FL&facets[location][]=GA&facets[location][]=HI&facets[location][]=IA&facets[location][]=ID&facets[location][]=IL&facets[location][]=IN&facets[location][]=KS&facets[location][]=KY&facets[location][]=LA&facets[location][]=MA&facets[location][]=MD&facets[location][]=ME&facets[location][]=MI&facets[location][]=MN&facets[location][]=MO&facets[location][]=MS&facets[location][]=MT&facets[location][]=NC&facets[location][]=ND&facets[location][]=NE&facets[location][]=NH&facets[location][]=NJ&facets[location][]=NM&facets[location][]=NV&facets[location][]=NY&facets[location][]=OH&facets[location][]=OK&facets[location][]=OR&facets[location][]=PA&facets[location][]=RI&facets[location][]=SC&facets[location][]=SD&facets[location][]=TN&facets[location][]=TX&facets[location][]=UT&facets[location][]=VA&facets[location][]=VT&facets[location][]=WA&facets[location][]=WI&facets[location][]=WV&facets[location][]=WY&facets[sectorid][]=99&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000&out=json"
    response = requests.get(url).json()
    
    # dict of data is inside of another nested list 'response'
    data = response['response']['data']
    df = pd.DataFrame.from_records(data)
    return df

#SECTION 2: Processing dataframes from API queries into what is needed for visualizations. 

def general_netgen_df(df):
    """
    Generates a dataframe with years from 2001 to 2022 as the index and
    fuel types as the columns and fills it with the respective generation
    values from get_general_netgen_data. Returns a dataframe.
    """
    fueltypes = df.fuelTypeDescription.unique()
    new_df = pd.DataFrame(index = range(2001, 2022), columns = fueltypes)
    
    for year in new_df.index:
        for col in new_df.columns:
            val = df.loc[(df['period'] == year) & (df['fuelTypeDescription'] == col)] # subset df
            val = val.set_index(['period']) # changes index to year so .loc can be used for next line
            new_df.loc[year, col] = val.loc[year, 'generation'] # assign generation number to new df
    return new_df

def netgen_by_sector_df(df):
    """
    Generates a dataframe with sectors as the index and fuel types as the
    columns and fills it with the respective generation values from the raw
    dataframe from get_netgen_by_sector. Returns a dataframe.
    """
    fueltypes = df.fuelTypeDescription.unique()
    sectors = df.sectorDescription.unique()
    new_df = pd.DataFrame(index=sectors, columns=fueltypes)
    for fuel in fueltypes:
        for sector in sectors:
            val = df.loc[(df['fuelTypeDescription'] == fuel) & (df['sectorDescription'] == sector)] # subset df
            if len(val.index) > 0: # checks that there's something in the subset row
                val = val.set_index(['period']) # changes index to year so .loc can be used in next line
                new_df.loc[sector, fuel] = val.loc[2022, 'generation']
            else: 
                continue
    return new_df

def netgen_by_state_df(df):
    """
    Generates a dataframe with US states and DC as the index and fuel types as
    the columns. Fills in the respective cells with the generation values from
    the raw dataframe from get_netgen_by_state. Returns a dataframe. 
    """
    fueltypes = df.fuelTypeDescription.unique()
    states = df.location.unique()
    new_df = pd.DataFrame(index = states, columns = fueltypes)
    for fuel in fueltypes:
        for state in states:
            for year in new_df.columns:
                val = df.loc[(df['fuelTypeDescription'] == fuel) & (df['location'] == state)] # subset df
                if len(val.index) > 0: # checks that there's a row in subset df
                    val = val.set_index(['period']) # sets index to year so .loc can be used in next line
                    new_df.loc[state, fuel] = val.loc[2022, 'generation']
    return new_df
"""
SECTION 3: Generating visualizations using matplotlib
"""

def general_netgen_viz(df):
    pass

def netgen_by_sector_viz(df):
    pass

def netgen_by_state_viz(df):
    pass
