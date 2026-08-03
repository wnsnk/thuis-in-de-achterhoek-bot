import json


def load_filters():
    with open('filters.json', 'r') as filters:
        filters = json.load(filters)
