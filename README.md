# Volley-grids

**Please note:** Volley-grids is still an active work in progress, do not expect it to be complete.


## Description

Volley-grids is a simple python library that allows you to create tournaments brackets for beach volleyball.


## Installation

Install using `pip install -U volley-grids`.

## Usage

```python
from pprint import pprint
from volley_grids.models.players import WomenPlayer, MenPlayer
from volley_grids.seeders.king_of_the_beach import KingOfTheBeachSeeder


# Create players
rebecca = WomenPlayer(name='Rebecca', surname='Silva')
melissa = WomenPlayer(name='Melissa', surname='Hummel')
john = MenPlayer(name='John', surname='Doe')
cristian = MenPlayer(name='Cristian', surname='Pereira')

# seed games
matches = KingOfTheBeachSeeder(participants=(rebecca, melissa, john, cristian,), match_type='full').seed()
pprint(matches)
#> [Silva R./Hummel M. VS Doe J./Pereira C.,
# Silva R./Doe J. VS Hummel M./Pereira C.,
# Silva R./Pereira C. VS Hummel M./Doe J.]
```