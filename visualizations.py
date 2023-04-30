"""
Miguel Candido Aurora Peralta
ISTA 350 Final Project Spring 2023

Generates three visualizations regarding generation of electricity using data
obtained from the US Energy Information Administration API.
"""

import requests
import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
from matplotlib.widgets import RadioButtons
from matplotlib.gridspec import GridSpec

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
    
    print("Getting data from API...")

    url = f"https://api.eia.gov/v2/electricity/electric-power-operational-data/data/?api_key={key}&frequency=annual&data[0]=generation&start=2009&end=2022&facets[fueltypeid][]=BIO&facets[fueltypeid][]=COW&facets[fueltypeid][]=GEO&facets[fueltypeid][]=HYC&facets[fueltypeid][]=NG&facets[fueltypeid][]=NUC&facets[fueltypeid][]=PC&facets[fueltypeid][]=PEL&facets[fueltypeid][]=SUN&facets[fueltypeid][]=WND&facets[location][]=US&facets[sectorid][]=99&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000&out=json"
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

    print('Getting data from API...')

    url = f"https://api.eia.gov/v2/electricity/electric-power-operational-data/data/?api_key={key}&frequency=annual&data[0]=generation&start=2010&end=2022&facets[fueltypeid][]=BIO&facets[fueltypeid][]=COW&facets[fueltypeid][]=GEO&facets[fueltypeid][]=HYC&facets[fueltypeid][]=NG&facets[fueltypeid][]=NUC&facets[fueltypeid][]=PC&facets[fueltypeid][]=PEL&facets[fueltypeid][]=SUN&facets[fueltypeid][]=WND&facets[location][]=US&&facets[sectorid][]=1&facets[sectorid][]=94&facets[sectorid][]=96&facets[sectorid][]=97&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000&out=json"
    response = requests.get(url).json()

    # dict of data is inside of another nested list 'response'
    data = response['response']['data']
    df = pd.DataFrame.from_records(data)
    return df

def get_netgen_by_state(key):
    """
    Given an EIA API key, returns a dataframe. Dataframe contains the net
    generation of electricity separated by generation method (solar, wind,
    etc.), and mainland US state + District of Columbia.
    """
    print("Getting data from API...")
    url = f"https://api.eia.gov/v2/electricity/electric-power-operational-data/data/?api_key={key}&frequency=annual&data[0]=generation&start=2021&end=2022&facets[fueltypeid][]=BIO&facets[fueltypeid][]=COW&facets[fueltypeid][]=GEO&facets[fueltypeid][]=HYC&facets[fueltypeid][]=NG&facets[fueltypeid][]=NUC&facets[fueltypeid][]=PC&facets[fueltypeid][]=PEL&facets[fueltypeid][]=SUN&facets[fueltypeid][]=WND&facets[location][]=AL&facets[location][]=AR&facets[location][]=AZ&facets[location][]=CA&facets[location][]=CO&facets[location][]=CT&facets[location][]=DC&facets[location][]=DE&facets[location][]=FL&facets[location][]=GA&facets[location][]=IA&facets[location][]=ID&facets[location][]=IL&facets[location][]=IN&facets[location][]=KS&facets[location][]=KY&facets[location][]=LA&facets[location][]=MA&facets[location][]=MD&facets[location][]=ME&facets[location][]=MI&facets[location][]=MN&facets[location][]=MO&facets[location][]=MS&facets[location][]=MT&facets[location][]=NC&facets[location][]=ND&facets[location][]=NE&facets[location][]=NH&facets[location][]=NJ&facets[location][]=NM&facets[location][]=NV&facets[location][]=NY&facets[location][]=OH&facets[location][]=OK&facets[location][]=OR&facets[location][]=PA&facets[location][]=RI&facets[location][]=SC&facets[location][]=SD&facets[location][]=TN&facets[location][]=TX&facets[location][]=UT&facets[location][]=VA&facets[location][]=VT&facets[location][]=WA&facets[location][]=WI&facets[location][]=WV&facets[location][]=WY&facets[sectorid][]=99&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000&out=json"
    response = requests.get(url).json()
    
    # dict of data is inside of another nested list 'response'
    data = response['response']['data']
    df = pd.DataFrame.from_records(data)
    return df

#SECTION 2: Processing dataframes from API queries into what is needed for visualizations. 

def general_netgen_df(df):
    """
    Generates a dataframe with fuel types as the index and years from 2001 to
    2022 as the columns. Fills it with the respective generation values from
    get_general_netgen_data. Returns a dataframe.
    """

    print("Processing data...")

    fueltypes = df.fuelTypeDescription.unique()
    new_df = pd.DataFrame(index = range(2010, 2022), columns = fueltypes)
    
    for year in new_df.index:
        for fuel in new_df.columns:
            val = df.loc[(df['period'] == year) & (df['fuelTypeDescription'] == fuel)] # subset df
            if len(val.index) > 0:
                val = val.set_index(['period']) # changes index to year so .loc can be used for next line
                new_df.loc[year, fuel] = val.loc[year, 'generation'] # assign generation number to new df
            else:
                continue
    return new_df

def netgen_by_sector_df(df):
    """
    Generates a dataframe with sectors as the index and fuel types as the
    columns and fills it with the respective generation values from the raw
    dataframe from get_netgen_by_sector. Returns a dataframe.
    """

    print('Processing data...')

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
    Generates a geopandas GeoDataFrame that contains the boundaries of all
    mainland US
    states read from a GeoJSON file, and fills in the dataframe with the energy 
    generation data with the energy sources added as columns.
    Returns a GeoDataFrame.
    """

    print("Processing data...")
    fueltypes = df.fuelTypeDescription.unique()
    states = df.stateDescription.unique()

    # creates geopandas GeoDataFrame from a GeoJSON file containing the
    # boundaries of all US states
    states_gdf = gpd.read_file("https://eric.clst.org/assets/wiki/uploads/Stuff/gz_2010_us_040_00_20m.json")
    states_gdf = states_gdf.set_index(['NAME']) # make index state names
    
    for fuel in fueltypes:
        for state in states:
            val = df.loc[(df['fuelTypeDescription'] == fuel) & (df['stateDescription'] == state)] # subset df
            if len(val.index) > 0: # checks that there's a row in subset df
                val = val.set_index(['period']) # sets index to year so .loc can be used in next line
                states_gdf.loc[state, fuel] = val.loc[2022, 'generation']
    states_gdf.drop(index=['Puerto Rico', 'Hawaii', 'Alaska']) # don't have energy data for puerto rico
    return states_gdf

"""
SECTION 3: Generating visualizations using matplotlib
"""

def general_netgen_viz(key):
    """
    Generates a stacked bar chart with year as the x axis and energy generation
    in GWh as the y axis. The pieces of each stacked bar
    represent sources of energy. 
    
    Argument df is a dataframe with years as the index and fuel types as the columns.
    """

    print("Starting figure 1...")
    df = general_netgen_df(get_general_netgen_data(key))
    print("Creating chart...")

    # sorts df columns by their mean value
    df = df.reindex(df.mean().sort_values().index, axis=1)

    fig, ax = plt.subplots(1,1)
    df.plot.bar(stacked=True, ax=ax, fontsize=10)

    ax.xaxis.set_label_position('top') # puts title above exponent label
    ax.set_title("Net electricity generation in the US from 2010-2022")
    ax.set_xlabel("Year")
    ax.set_ylabel('Net generation (GWh)', fontsize=12)

    ax.legend(loc=2, bbox_to_anchor=(1.05, 1.0), fontsize=10)
    # change with of ax to fit legend
    pos = ax.get_position()
    ax.set_position([pos.x0, pos.y0, pos.width * 1.0, pos.height])
    fig.set_figwidth(8)
    plt.tight_layout()
    
    print("Completed Figure 1: Net electricity generation in the US from 2010-2022\n")

def netgen_by_sector_viz(key):
    """
    Generates a stacked bar chart with the sector as the x axis and the net
    energy generation in thousand megawatthours as the y axis. The pieces of
    each stacked bar represent the sources of energy.

    Argument df is a dataframe with the sectors as the index values and fuel types as the columns. 
    """

    print('Starting Figure 2...')
    df = netgen_by_sector_df(get_netgen_by_sector(key))
    print('Creating chart...')

    # sorts df columns by their mean value
    df = df.reindex(df.mean().sort_values().index, axis=1)

    fig, ax = plt.subplots(1,1)
    df.plot.bar(stacked=True, ax=ax, fontsize=10)
    
    # put "Independent Power Producers" on separate lines
    xt = list(df.index)
    xt[2] = '\n'.join(xt[2].split())
    # apply above changes and make the x labels horizontal
    ax.set_xticklabels(xt, rotation=0)

    ax.set_xlabel('Sector', fontsize=14)
    ax.set_ylabel('Net generation (GWh)', fontsize=12)

    ax.set_title("Net electricity generation by sector in 2022")
    
    ax.legend(loc=2, bbox_to_anchor=(1.05, 1.0), fontsize=10)
    # change with of ax to fit legend
    pos = ax.get_position()
    ax.set_position([pos.x0, pos.y0, pos.width * 0.98, pos.height])
    fig.set_figwidth(9)
    plt.tight_layout()
    
    print('Completed Figure 2: Net electricity generation by sector in 2022\n')

def netgen_by_state_viz(key):
    """
    Generates an interactive choropleth visualization of the net electricity
    generation by state. Allows user to select the energy source to be
    displayed. 
    """
    print("Starting Figure 3...")
    gdf = netgen_by_state_df(get_netgen_by_state(key)) 
    print("Creating chart...")

    fig, ax = plt.subplots()
    fig.set_figwidth(10)

    # creates radiobutton ax on fig
    rax = fig.add_axes([0.04, 0.15, 0.27, 0.35])
    fuels = list(gdf.columns[5:]) # pulls list of fuels for button labels from df
    radio = RadioButtons(rax, labels=fuels, activecolor='maroon')
    for circle in radio.circles:
        circle.set_radius(0.035)
        

    gdf.plot(column='biomass', cmap = 'OrRd', scheme='QUANTILES', edgecolor = 'k', ax=ax, legend=True, legend_kwds={'loc': 'center right', 'bbox_to_anchor':(-.115,0.85)})
    ax.set_title(f"Net generation (GWh) from biomass in the continental US")
    plt.subplots_adjust(left = 0.35) # moves map right

    def energy_source(label):
        ''' Function performed on selection of a radio button '''
        ax.set_title(f"Net generation (GWh) from {label} in the continental US")
        gdf.plot(column=label, cmap = 'OrRd', scheme='QUANTILES', edgecolor = 'k', ax=ax, legend=True, legend_kwds={'loc': 'center right', 'bbox_to_anchor':(-.115,0.85)})

    radio.on_clicked(energy_source)
    plt.show()

    print("Completed Figure 2: Interactive Choropleth Map\n")
    

def main():
    """ Displays visualizations. """
    key = "M75XbnCHbwIymVSeZUs2eVbnKlhd4EmWraupMZ5c"
    general_netgen_viz(key)
    netgen_by_sector_viz(key)
    netgen_by_state_viz(key)
    plt.show()

main()