import random

def calculate_food_miles(customer_postcode, producer_postcode):
    """Calculate approximate food miles between customer and producer"""
    if not customer_postcode or not producer_postcode:
        return None
    
    # Simple hash-based distance for demo (2-25 miles range)
    random.seed(hash(customer_postcode + producer_postcode) % 100)
    return round(random.uniform(2, 25), 1)
