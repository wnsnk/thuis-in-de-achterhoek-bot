# ERRORS

```
Total listings found: 0
Found 0 available listings.
Total listings found: 3
Found 2 available listings.
Traceback (most recent call last):
  File "thuis in de achterhoek/main.py", line 118, in <module>
    'arguments[0].scrollIntoView();', eligible_listings[0])
                                      ~~~~~~~~~~~~~~~~~^^^
TypeError: 'NoneType' object is not subscriptable
```
old code:
```py
    if len(available_listings) != 0:
        return available_listings
    else:
        # TODO Find a good way to retry this
        get_eligible_listings()
        time.sleep(1)
```
current fix: 
```py
    if len(available_listings) != 0:
        return available_listings
    else:
        # TODO Find a good way to retry this
        available_listings = get_eligible_listings()
        time.sleep(1)
        return available_listings
```