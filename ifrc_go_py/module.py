import requests
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
from collections import Counter
from datetime import datetime

class InvalidDateFormatError(Exception):
    pass

class SurgeAlert:
    def __init__(self, alert_id, message, molnix_id, created_at, opens, closes, start, end, region, modality, sector, scope, language, rotation, event_name, event_id, country_code):
        self.alert_id = alert_id
        self.message = message
        self.molnix_id = molnix_id
        self.created_at = created_at
        self.opens = opens
        self.closes = closes
        self.start = start
        self.end = end
        self.region = region
        self.modality = modality
        self.sector = sector
        self.scope = scope
        self.language = language
        self.rotation = rotation
        self.event_name = event_name
        self.event_id = event_id
        self.country_code = country_code
        
    def __repr__(self):
        return f"SurgeAlert(alert_id={self.alert_id}, {self.message})"
    
class Appeal:
    def __init__(self, aid, name, atype, atype_display, status, status_display, code, sector, num_beneficiaries, amount_requested, amount_funded, start_date, end_date, created_at, event, dtype_name, country_iso3, country_society_name):
        self.aid = aid
        self.name = name
        self.atype = atype
        self.atype_display = atype_display
        self.status = status
        self.status_display = status_display
        self.code = code
        self.sector = sector
        self.num_beneficiaries = num_beneficiaries
        self.amount_requested = amount_requested
        self.amount_funded = amount_funded
        self.start_date = start_date
        self.end_date = end_date
        self.created_at = created_at
        self.event = event
        self.dtype_name = dtype_name
        self.country_iso3 = country_iso3
        self.country_society_name = country_society_name

def get_all_appeals():
    """
    Returns the 50 latest appeals, with option to filter by appeal type.
    
    """
    api_call = 'https://goadmin.ifrc.org/api/v2/appeal'
    appeals = []
    current_page = 0
    print("Grabbing all appeals. This requires looping over several dozen pages of results, so it may take some time.")
    
    while api_call:
        current_page += 1
        print(f"Fetching page {current_page} from {api_call}") 
        
        response = requests.get(api_call).json()
        results = response.get('results', [])
        
        for result in results:
            appeal = Appeal(
                result.get('aid'), result.get('name'), result.get('atype'), result.get('atype_display'),
                result.get('status'), result.get('status_display'), result.get('code'), result.get('sector'),
                result.get('num_beneficiaries'), result.get('amount_requested'), result.get('amount_funded'),
                result.get('start_date'), result.get('end_date'), result.get('created_at'), result.get('event'),
                result.get('dtype_name'), result.get('country', {}).get('iso3'),
                result.get('country', {}).get('society_name')
            )
            appeals.append(appeal)
            
        api_call = response.get('next')  # fetch next page URL
        
    return appeals

def search_appeals(atype=None, start_date=None, end_date=None, emergency_type=None):
    """
    Returns appeals matching the search criteria passed as arguments.
    
    Args:
        atype (int or None, optional): The appeal type to filter the appeals. 
            0 = DREF
            1 = Emergency Appeal
    
            If provided, filters the appeals based on the specified type. 
            Defaults to None, retrieving all appeals if no type is specified.
        
        start_date (str or None, optional): The min start date to filter by.
            Format as %Y-%m-%d (e.g. "2024-01-01")
        
        end_date (str or None, optional): The max end date to filter by.
            Format as %Y-%m-%d (e.g. "2024-01-01")
            
        emergency_type (int or None, optional): Use the IFRC emergency type to filter:
            (66	Biological)
            (57	Chemical)
            (7	Civil Unrest)
            (14	Cold Wave)
            (6	Complex Emergency)
            (4	Cyclone)
            (20	Drought)
            (2	Earthquake)
            (1	Epidemic)
            (15	Fire)
            (12	Flood)
            (21	Food Insecurity)
            (19	Heat Wave)
            (62	Insect Infestation)
            (24	Landslide)
            (13	Other)
            (27	Pluvial/Flash Flood)
            (5	Population Movement)
            (67	Radiological)
            (23	Storm Surge)
            (54	Transport Accident)
            (68	Transport Emergency)
            (11	Tsunami)
            (8	Volcanic Eruption)
    """
    
    api_call = 'https://goadmin.ifrc.org/api/v2/appeal'
    
    params = []

    if atype is not None:
        params.append(f'atype={atype}')
        
    if start_date is not None:
        if len(start_date) != 10:
            raise InvalidDateFormatError("Start date should be in '%Y-%m-%d' format, like 2020-04-04.")
        else:
            start_date = start_date + 'T00:00:00Z'
            params.append(f'start_date__gt={start_date}')
        
    if end_date is not None:
        if len(end_date) != 10:
            raise InvalidDateFormatError("End date should be in '%Y-%m-%d' format, like 2020-04-04.")
        else:
            end_date = end_date + 'T00:00:00Z'
            params.append(f'end_date__lt={end_date}')
        
    if emergency_type is not None:
        params.append(f'dtype={emergency_type}')
        
    if params:
        api_call += '?' + '&'.join(params)
        
    print(api_call)
    
    r = requests.get(api_call).json()
    appeals = []
    
    for result in r['results']:
        aid = result.get('aid')
        name = result.get('name')
        atype = result.get('atype')
        atype_display = result.get('atype_display')
        status = result.get('status')
        status_display = result.get('status_display')
        code = result.get('code')
        sector = result.get('sector')
        num_beneficiaries = result.get('num_beneficiaries')
        amount_requested = result.get('amount_requested')
        amount_funded = result.get('amount_funded')
        start_date = result.get('start_date')
        end_date = result.get('end_date')
        created_at = result.get('created_at')
        event = result.get('event')
        dtype_name = result.get('dtype_name')
        country_info = result.get('country', {})
        country_iso3 = country_info.get('iso3')
        country_society_name = country_info.get('society_name')
        
        # create appeal object and append to appeals list
        appeal = Appeal(aid, name, atype, atype_display, status, status_display, code, sector, num_beneficiaries, amount_requested, amount_funded, start_date, end_date, created_at, event, dtype_name, country_iso3, country_society_name)
        appeals.append(appeal)
        
        
    return appeals

def plot_countries_by_iso3(appeals):
    """
    Pass in a list of Appeal objects and generate a map at admin0 countries.
    
    Args:
        None
    """
    
    iso3_countries = [appeal.country_iso3 for appeal in appeals if appeal.country_iso3]
    
    if not iso3_countries:
        print("No ISO3 country codes found in the provided data.")
        return
    
    # remove Antarctica from the list of iso3 codes
    iso3_countries = [iso for iso in iso3_countries if iso != 'ATA']
    
    iso3_counter = Counter(iso3_countries)
    
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    
    world_iso3 = world.merge(
        pd.DataFrame.from_dict(iso3_counter, orient='index', columns=['Appeal_Count']).reset_index(),
        how='left',
        left_on='iso_a3',
        right_on='index'
    )
    
    world_iso3['Appeal_Count'] = world_iso3['Appeal_Count'].fillna(0)
    
    # remove antarctica from the map data
    world_iso3 = world_iso3[world_iso3['continent'] != 'Antarctica']
    
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    
    # plot the map
    ax.axis('off')
    ax.set_title('Choropleth Map of Appeals per Country')
    
    world_iso3.plot(column='Appeal_Count', ax=ax, legend=True, cmap='viridis', 
                    legend_kwds={'label': "Number of Appeals", 'orientation': "horizontal",
                                 'ticks': range(0, int(world_iso3['Appeal_Count'].max()) + 1)},
                    edgecolor='none')  # Remove boundary lines
    
    # filter out antarctica
    world_iso3[world_iso3['Appeal_Count'] == 0].plot(ax=ax, color='lightgrey')
    
    plt.tight_layout()  # this removes the spacing and border around the map
    plt.show()
