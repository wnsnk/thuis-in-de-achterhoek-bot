import json
from .listing_details import listingDetails


def load_filters():
    with open('filters.json', 'r') as filters:
        filters = json.load(filters)
        return filters


def sort_by():
    sort_by = load_filters()['sort_by']
    sort_by_dict = {'price low-high': '#?gesorteerd-op=prijs%2B',
                    'price high-low': '#?gesorteerd-op=prijs-',
                    'city a-z': '#?gesorteerd-op=plaats%2B',
                    'city z-a': '#?gesorteerd-op=plaats-',
                    'neighborhood a-z': '#?gesorteerd-op=wijk%2B',
                    'neighborhood z-a': '#?gesorteerd-op=wijk-',
                    'house type a-z': '#?gesorteerd-op=woningtype%2B',
                    'house type z-a': '#?gesorteerd-op=woningtype-',
                    'respond time': '?gesorteerd-op=reactiedatum-',
                    'newest': '#?gesorteerd-op=publicatiedatum-'}
    return sort_by_dict[sort_by]


def check_listing(listing_details: listingDetails):
    filters = load_filters()

    if listing_details.price > filters['max_price_per_month']:
        return False
    elif listing_details.m2 < filters['min_m2']:
        return False
    elif listing_details.bedrooms < filters['min_bedrooms']:
        return False
    elif listing_details.listing_type not in filters['listing_type']:
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
    # TODO: Add elderly home
    else:
        return True
