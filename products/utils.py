import math
from geopy.distance import distance
from geopy.geocoders import Nominatim

# Simple food miles calculation (TC-013)
def calculate_food_miles(producer_postcode, customer_postcode):
    """
    Calculate approximate distance between producer and customer.
    Uses postcode areas for estimation.
    """
    if not producer_postcode or not customer_postcode:
        return None
    
    # Simple lookup table for Bristol area postcodes
    # In production, you'd use a geocoding API
    postcode_areas = {
        'BS1': (51.4545, -2.5879),  # Bristol city centre
        'BS2': (51.4600, -2.5800),
        'BS3': (51.4400, -2.5900),
        'BS4': (51.4300, -2.5500),
        'BS5': (51.4600, -2.5400),
        'BS6': (51.4700, -2.6000),
        'BS7': (51.4800, -2.5700),
        'BS8': (51.4600, -2.6200),
        'BS9': (51.4900, -2.6300),
        'BS10': (51.5000, -2.6100),
        'BS11': (51.5100, -2.6800),
        'BS13': (51.4100, -2.6100),
        'BS14': (51.4200, -2.5700),
        'BS15': (51.4600, -2.5100),
        'BS16': (51.4900, -2.5200),
        'BS20': (51.4800, -2.7200),
        'BS21': (51.4400, -2.8500),
        'BS22': (51.3600, -2.9300),
        'BS23': (51.3500, -2.9800),
        'BS24': (51.3200, -2.9700),
        'BS25': (51.3000, -2.8300),
        'BS26': (51.2800, -2.8600),
        'BS27': (51.2800, -2.7700),
        'BS28': (51.2500, -2.8200),
        'BS29': (51.2800, -2.8900),
        'BS30': (51.4400, -2.4700),
        'BS31': (51.4100, -2.5000),
        'BS32': (51.5400, -2.5600),
        'BS34': (51.5200, -2.5600),
        'BS35': (51.5900, -2.5400),
        'BS36': (51.5200, -2.4700),
        'BS37': (51.5400, -2.4200),
        'BS39': (51.3600, -2.5200),
        'BS40': (51.3600, -2.6800),
        'BS41': (51.4300, -2.6500),
        'BS48': (51.4300, -2.7400),
        'BS49': (51.3900, -2.8100),
    }
    
    # Extract area from postcode (e.g., BS1 from BS1 5JG)
    producer_area = producer_postcode.split()[0] if ' ' in producer_postcode else producer_postcode[:3]
    customer_area = customer_postcode.split()[0] if ' ' in customer_postcode else customer_postcode[:3]
    
    if producer_area in postcode_areas and customer_area in postcode_areas:
        prod_coords = postcode_areas[producer_area]
        cust_coords = postcode_areas[customer_area]
        
        # Calculate distance using haversine formula (simplified)
        lat1, lon1 = prod_coords
        lat2, lon2 = cust_coords
        
        # Approximate distance in miles (1 degree ≈ 69 miles)
        lat_diff = abs(lat1 - lat2) * 69
        lon_diff = abs(lon1 - lon2) * 69 * math.cos(math.radians((lat1 + lat2) / 2))
        distance = math.sqrt(lat_diff**2 + lon_diff**2)
        
        return round(distance, 1)
    
    return None
