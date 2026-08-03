# thuis-in-de-achterhoek-bot

## Description

A bot made with selenium that automates applying for housing via Thuis In De Achterhoek.

## Status:

- Log in ✔️
- Check current amount of outgoing applications (max 3) ✔️
- If outgoing applications < 3:
  - Check listings for not yet applied housing ✔️
  - Submit Applications ✔️
- Filter appartments based on your preference ✔️
- Add Error handling ✔️

## TODO:

- Remove unnecessary time.sleeps
- Test program with different browsers

## How to use:

### Installation

- clone the repository, create a virtual environment and install dependencies:

```bash
git clone https://github.com/wnsnk/thuis-in-de-achterhoek-bot.git

cd thuis-in-de-achterhoek-bot

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

- Make sure you have installed Firefox (Future versions might support other browsers)

### Add your e-mail and password to a .env file.

1. Make a copy of .env.example and name it .env
2. add your thuis in de achterhoek username and password in the .env file

### Add filters (optional)

The standard filters will not remove anything.

- open filters.json

#### Example:

```json
{
  "sort_by": "respond time",
  "max_price_per_month": 1000,
  "min_m2": 10,
  "min_bedrooms": 2,
  "elderly_home": false,
  "listing_type": ["registration time", "lottery", "first to respond"],
  "city_blacklist": [],
  "only_ground_floor_or_elevator": false
}
```

#### sort_by (string)

This tells the program what listings to check first.

- Options:

```
'price low-high', 'price high-low', 'city a-z', 'city z-a','neighborhood a-z', 'neighborhood z-a', 'house type a-z', 'house type z-a', 'respond time', 'newest'
```

#### max_price_per_month (integer)

The maximum price per month you want to pay.

#### min_m2 (integer)

The minimum square meters (m2) the house should have.

#### min_bedrooms (integer)

The minimun bedrooms the house should have

#### elderly_home (boolean)

A 65+ home. You can also respond to these listings if you are younger. But the elderly have priority in these houses

- true if you want to respond to 65+ houses
- false if you don't want to respond to 65+ houses

#### listing_type (list)

Thuis in de Achterhoek has 3 listing types. The listing type decides the order of the candidates.

- Registration time (the longer your registration time for Thuis in de Achterhoek, the higher your position)
- Lottery (Every candidate has an equal chance and your position is chosen randomly)
- First to respond (The earlier you respond, the higher your position)

```json
"listing_type": ["registration time", "lottery", "first to respond"]
```

listing_type should always be a list/array. Even if you only want to respond to 1 listing type.
For example:

```json
"listing_type": ["lottery"]
```

#### city_blacklist (list)

If you absolutely don't want to live in a certain town/city. You can put the name of the town/city here.
city_blacklist should always be a list/array. Even if you only want to blacklist 1 town/city or don't want to blacklist anything.

```json
"city_blacklist": ["doetinchem"]
```

#### only_ground_or_elevator (boolean)

should be either true or false.

- true (This will remove all appartments without a elevator. Houses/Appartments on the ground floor will not be removed)
- false (if you want to respond to a house/ appartment regardless of a elevator)

### Run the app:

```bash
python main.py
```

## Tech Stack

- Python 3.14
- Selenium
- Beautiful Soup
