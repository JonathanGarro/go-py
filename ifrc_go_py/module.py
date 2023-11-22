import requests

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
        
def get_latest_surge_alerts():
    """
    Returns the 50 latest surge alerts.
    
    >>> get_latest_surge_alerts()
    [SurgeAlert(alert_id=18541, message=Humanitarian Diplomacy Coordinator, Middle East Crisis, MENA), SurgeAlert(alert_id=18540, message=Finance Officer, Hurricane Otis, Mexico.)...]
    """
    
    api_call = 'https://goadmin.ifrc.org/api/v2/surge_alert/'
    r = requests.get(api_call).json()
    
    surge_alerts = []
    
    for result in r['results']:
        alert_id = result['id']
        message = result['message']
        molnix_id = result['molnix_id']
        created_at = result['created_at']
        opens = result['opens']
        closes = result['closes']
        start = result['start']
        end = result['end']
        
        region, modality, sector, scope, language, rotation, event_name, event_id, country_code = '', '', '', '', '', '', '', '', ''
        
        for tag in result['molnix_tags']:
            groups = tag['groups']
            if 'LANGUAGE' in groups:
                language = tag['description']
            if 'rotation' in groups:
                rotation = tag['description']
            if 'ALERT TYPE' in groups:
                scope = tag['description']
            if 'Modality' in groups:
                modality = tag['description']
            if 'REGION' in groups:
                region = tag['description']
            if 'OPERATIONS' in groups:
                event_name = tag['description']
                event_id = tag['name']
            if 'ROLES' in groups:
                try:
                    next_index = groups.index('ROLES') + 1
                    sector = groups[next_index]
                except IndexError:
                    sector = 'Missing Sector'
                    
        try:
            country_code = result['event']['countries'][0]['iso3']
        except:
            country_code = 'Missing Country'
            
        # create SurgeAlert object and append to surge_alerts list
        surge_alert = SurgeAlert(alert_id, message, molnix_id, created_at, opens, closes, start, end, region, modality, sector, scope, language, rotation, event_name, event_id, country_code)
        surge_alerts.append(surge_alert)
        
    return surge_alerts
