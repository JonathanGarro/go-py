import requests
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
from collections import Counter

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
        return f"SurgeAlert(alert_id={self.alert_id}, message={self.message})"

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

def get_latest_appeals(atype=None):
    """
    Returns the 50 latest appeals, with option to filter by appeal type.
    
    Args:
        atype (int or None, optional): The appeal type to filter the appeals. 
            0 = DREF
            1 = Emergency Appeal
    
            If provided, filters the appeals based on the specified type. 
            Defaults to None, retrieving all appeals if no type is specified.
    
    >>> get_latest_appeals()
    [Appeal(alert_id=18541, message=Humanitarian Diplomacy Coordinator, Middle East Crisis, MENA), SurgeAlert(alert_id=18540, message=Finance Officer, Hurricane Otis, Mexico.)...]
    """
    
    if atype is not None:
        api_call = f'https://goadmin.ifrc.org/api/v2/appeal/?atype={atype}'
    else:
        api_call = 'https://goadmin.ifrc.org/api/v2/appeal/'
    
    r = requests.get(api_call).json()
    print(r)
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
    
    plt.tight_layout()  # Adjust layout for better visualization
    plt.show()