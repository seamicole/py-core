# Python Core Utilities
##### A Fully-typed Core Utility Suite Written in Python

> There should be one -- and preferably only one -- obvious way to do it.

## Installation

You know the drill:

```bash
pip install python-core-utilities
```

> Just Do It ✓

## Collection

An abstract container intended to store a collection of items in an arbitrary data structure.

> If you were a list, a Collection would be her ex.

### DictCollection

A dictionary-based collection utility class with integrated support for efficient key lookups.

```python
from core.collection import DictCollection

class Country:
    """A class that represents countries of the world"""

    def __init__(self, name: str, iso2: str, iso3: str):
        """Init Method"""

        self.name = name
        self.iso2 = iso2
        self.iso3 = iso3

    def __str__(self) -> str:
        """String Method"""

        return self.name

# Initialize a countries DictCollection
countries = DictCollection[Country](keys=("iso2", "iso3"))

# Iterate over countries to create
for name, iso2, iso3 in (
    ("Cambodia", "KH", "KHM"),
    ("China", "CN", "CHN"),
    ("Fiji", "FJ", "FJI"),
    ("Guam", "GU", "GUM"),
    ("Singapore", "SG", "SGP"),
    ("Thailand", "TH", "THA"),
    ("United States", "US", "USA"),
):
    # Initialize country instance
    country = Country(name=name, iso2=iso2, iso3=iso3)

    # Add country to countries collection
    countries.add(country)

# Print countries
print(countries)

# <DictCollection: 7 [Cambodia, China, Fiji, Guam, Singapore, Thailand, United States]>
```

Retrieve items by any of their keys:

```python
# Look up Thailand by ISO2
print(countries["TH"], repr(countries["TH"]))

# Thailand <__main__.Country object at 0x7f8d085e2560>

# Look up Thailand by ISO3
print(countries["THA"], repr(countries["THA"]))

# Thailand <__main__.Country object at 0x7f8d085e2560>
```

A sense of familiarity in behavior is always a nice touch:

```python
# Attempt to retrieve a non-existent country by key
countries["XYZ"]

# core.collection.exceptions.NonExistentKeyError: Non-existent key detected: 'XYZ'

try:
    countries["XYZ"]
except KeyError:
    print("Just a KeyError under the hood!")

# Just a KeyError under the hood!

# Retrieve a non-existent country by key with a dict-like 'get'
countries.get("XYZ")

# None

# Provide a default country if applicable
countries.get("XYZ", countries["THA"])

# Thailand

# CAVEAT: The get method assumes a return value of the collection generic
# i.e. countries.get(key: Hashable, default: Country | Hashable | None) -> Country | None

# ... did you catch the spoiler?
```

Keys are treated as synonymous with the items to which they are associated:

```python
# Retrieve Thailand country instance
thailand = countries["THA"]

# Show that she is present in the countries collection
print(repr(thailand), "in countries:", thailand in countries)

# <__main__.Country object at 0x7f8d085e2560> in countries: True

# Show that this works in the same way with with just her ISO3 key
print("'THA' in countries:", "THA" in countries)

# 'THA' in countries: True
```

Naturally then, you may also remove items by any of their keys:

```python
# Remove Thailand by ISO2
countries.remove("TH")

# Print countries
print(countries)

# <DictCollection: 6 [Cambodia, China, Fiji, Guam, Singapore, United States]>

# Remove Singapore by ISO3
countries.remove("SGP")

# Print countries
print(countries)

# <DictCollection: 5 [Cambodia, China, Fiji, Guam, United States]>
```

> Don't be a dict, use a DictCollection.
