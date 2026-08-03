import json
from .listing_details import listingDetails


def load_filters():
    with open('filters.json', 'r') as filters:
        filters = json.load(filters)
        return filters


def check_listing(listing_details: listingDetails):
    filters = load_filters()
    if listing_details.price > filters['max_price_per_month']:
        print('check price')
        return False
    elif listing_details.m2 < filters['min_m2']:
        print('check m2')
        return False
    elif listing_details.bedrooms < filters['min_bedrooms']:
        print('check bedrooms')
        return False
    elif listing_details.listing_type not in filters['listing_type']:
        print('check listing type')
        return False
    elif filters['city_blacklist']:
        for city in filters['city_blacklist']:
            if listing_details.city.lower() == city.lower():
                print('check city blacklist')
                return False
    elif filters['only_ground_floor_or_elevator']:
        print('check floor')
        if listing_details.floor.lower() == 'begane grond':
            return True
        elif 'met lift' in listing_details.house_type:
            return True
        else:
            return False
    else:
        return True
