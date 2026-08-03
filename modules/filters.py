import json
from .listing_details import listingDetails
from .exceptions import NoTanslationError


def load_filters():
    with open('filters.json', 'r') as filters:
        filters = json.load(filters)
        return filters


filters = load_filters()


def sort_by():
    sort_by = filters['sort_by']
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
    if listing_details.price > filters['max_price_per_month']:
        return False
    if listing_details.m2 < filters['min_m2']:
        return False
    if listing_details.bedrooms < filters['min_bedrooms']:
        return False
    if listing_details.listing_type:
        translated_listing_types = translate_listing_type()
        if listing_details.listing_type not in translated_listing_types:
            return False
    if filters['city_blacklist']:
        for city in filters['city_blacklist']:
            if listing_details.city.lower() == city.lower():
                return False
    if filters['only_ground_floor_or_elevator']:
        if listing_details.floor.lower() == 'begane grond':
            return True
        elif 'met lift' in listing_details.house_type:
            return True
        else:
            return False

    # TODO: Add elderly home
    else:
        return True


def translate_listing_type():
    listing_type_english = filters['listing_type']
    listing_type_dutch = []
    for listing_type in listing_type_english:
        if listing_type.lower() == 'registration time':
            listing_type_dutch.append('Inschrijfduur')
        elif listing_type.lower() == 'lottery':
            listing_type_dutch.append('Loting')
        # elif listing_type.lower() == 'first to respond':
        #     # TODO: This listing type almost never happens. So i don't know yet what the translation should be.
        #     raise NoTanslationError(
        #         'No translation for this listing type. Please create a issue on the github repository. https://github.com/wnsnk/thuis-in-de-achterhoek-bot')
    return listing_type_dutch
