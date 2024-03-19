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

> For the collective good, as it were.

<details>

<summary><b>ListCollection</b></summary>

### ListCollection

A list-based collection utility class with intuitive methods that extend traditional list functionality.

```python
from core.collection import ListCollection

class Song:
    """A class that represents songs of someone with good taste in music"""

    def __init__(self, title: str, artist: str, year: int):
        """Init Method"""

        self.artist = artist
        self.title = title
        self.year = year

    def __str__(self) -> str:
        """String Method"""

        return f"{self.artist} | {self.title} ({self.year})"

# Initialize a songs ListCollection
songs = ListCollection[Song]()

# Add songs to songs collection
songs.add(
    Song(artist="Children of Bodom", title="Kissing the Shadows", year=2000),
    Song(artist="Dio", title="Holy Diver", year=1983),
    Song(artist="Dio", title="The Last In Line", year=1984),
    Song(artist="Disturbed", title="Overburdened", year=2005),
    Song(artist="Dream Theater", title="The Glass Prison", year=2002),
    Song(artist="Dream Theater", title="Breaking All Illusions", year=2011),
    Song(artist="Greta Van Fleet", title="Brave New World", year=2018),
    Song(artist="Greta Van Fleet", title="Built By Nations", year=2021),
    Song(artist="Iron Maiden", title="Revelations", year=1983),
    Song(artist="Iron Maiden", title="Brave New World", year=2000),
    Song(artist="Led Zeppelin", title="No Quarter", year=1983),
    Song(artist="Led Zeppelin", title="The Rover", year=2000),
    Song(artist="Queensrÿche", title="Eyes Of A Stranger", year=2000)
)

# Print songs
print(songs)

# <ListCollection: 13 [Children of Bodom | Kissing the Shadows (2000), Dio | Holy Diver (1983),
#                      Dio | The Last In Line (1984), Disturbed | Overburdened (2005),
#                      Dream Theater | The Glass Prison (2002),
#                      Dream Theater | Breaking All Illusions (2011),
#                      Greta Van Fleet | Brave New World (2018),
#                      Greta Van Fleet | Built By Nations (2021),
#                      Iron Maiden | Revelations (1983), Iron Maiden | Brave New World (2000),
#                      Led Zeppelin | No Quarter (1973), Led Zeppelin | The Rover (1975),
#                      Queensrÿche | Eyes Of A Stranger (1988)]>

```

Filter items by their attributes. Attribute **equals**:

```python
# Filter songs by title (strict / case-insensitive equality)
print(songs.filter(title="Brave New World"))
print(songs.filter(title__ieq="brave new world"))

# <ListCollection: 2 [Greta Van Fleet | Brave New World (2018),
#                     Iron Maiden | Brave New World (2000)]>
```

Attribute **contains**:

```python
# Filter songs by title (strict contains)
print(songs.filter(title__contains="Over"))

# <ListCollection: 1 [Disturbed | Overburdened (2005)]>

# Filter songs by title (case-insensitive contains)
print(songs.filter(title__icontains="over"))

# <ListCollection: 2 [Disturbed | Overburdened (2005), Led Zeppelin | The Rover (1975)]>
```

Attribute **is in**:

```python
# Filter songs by artist (strict / case-insensitive in)
print(songs.filter(artist__in=["Dream Theater", "Iron Maiden"]))
print(songs.filter(artist__iin=["dream theater", "IRON MAIDEN"]))

# <ListCollection: 4 [Dream Theater | The Glass Prison (2002),
#                     Dream Theater | Breaking All Illusions (2011),
#                     Iron Maiden | Revelations (1983), Iron Maiden | Brave New World (2000)]>
```

Attribute is **greater than / less than / equal to**:

```python
# Filter songs by year (greater than)
print(songs.filter(year__gt=2000))

# <ListCollection: 5 [Disturbed | Overburdened (2005), Dream Theater | The Glass Prison (2002),
#                     Dream Theater | Breaking All Illusions (2011),
#                     Greta Van Fleet | Brave New World (2018),
#                     Greta Van Fleet | Built By Nations (2021)]>

# Filter songs by year (greater than or equal to)
print(songs.filter(year__gte=2000))

# <ListCollection: 7 [Children of Bodom | Kissing the Shadows (2000),
#                     Disturbed | Overburdened (2005), Dream Theater | The Glass Prison (2002),
#                     Dream Theater | Breaking All Illusions (2011),
#                     Greta Van Fleet | Brave New World (2018),
#                     Greta Van Fleet | Built By Nations (2021),
#                     Iron Maiden | Brave New World (2000)]>

# Filter songs by year (less than)
print(songs.filter(year__lt=2000))

# <ListCollection: 6 [Dio | Holy Diver (1983), Dio | The Last In Line (1984),
#                     Iron Maiden | Revelations (1983), Led Zeppelin | No Quarter (1973),
#                     Led Zeppelin | The Rover (1975),
#                     Queensrÿche | Eyes Of A Stranger (1988)]>

# Filter songs by year (less than or equal to)
print(songs.filter(year__lte=2000))

# <ListCollection: 8 [Children of Bodom | Kissing the Shadows (2000), Dio | Holy Diver (1983),
#                     Dio | The Last In Line (1984), Iron Maiden | Revelations (1983),
#                     Iron Maiden | Brave New World (2000), Led Zeppelin | No Quarter (1973),
#                     Led Zeppelin | The Rover (1975),
#                     Queensrÿche | Eyes Of A Stranger (1988)]>
```

And of course by **multiple attributes**:

```python
# Filter songs by title and artist
print(songs.filter(title="Brave New World", artist="Iron Maiden"))

# <ListCollection: 1 [Iron Maiden | Brave New World (2000)]>

# Filter songs by title or artist
print(songs.filter(title__icontains="in") | songs.filter(artist__icontains="of"))

# <ListCollection: 3 [Children of Bodom | Kissing the Shadows (2000),
#                     Dio | The Last In Line (1984),
#                     Dream Theater | Breaking All Illusions (2011)]>
```

**Q.E.D. | Quite Easily Done.**

> If you were a list, the ListCollection would be her ex.

---

</details>

<details>

<summary><b>DictCollection</b></summary>

### DictCollection

A dictionary-based collection utility class with integrated support for efficient key lookups.

**...in addition** to all of the useful methods discussed above, of course!

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

Key unicity is enforced within a given collection:

```python
# Create a duplicate Thailand instance
thailand_duplicate = Country(name="Thailand Duplicate", iso2="TH", iso3="THA")

# Attempt to add the duplicate Thailand instance to the countries collection
countries.add(thailand_duplicate)

# core.collection.exceptions.DuplicateKeyError: Duplicate key detected: 'TH'
```

Retrieve existing items by any of their keys:

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
# Retrieve Thailand country instance by ISO3 key
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

**Q.E.D. | Quite Easily Done.**

> Don't be a dict, use a DictCollection.
---

</details>
