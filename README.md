# tcgbattle

Battle Pokémon TCG cards from the original [Base 1](https://pokemontcg.guru/set/base/base1) set against each other!  
Contains a CLI tool to initiate the battles, with results output to Slack.

![screenshot](https://user-images.githubusercontent.com/8943230/107743229-cd86cd00-6d10-11eb-848c-4e8a184c3d01.png)

## Battle Rules

* The first Pokémon passed into the CLI strikes first, and the two then alternate turns.
* Attacks are chosen by random, and only the damage number is taken into account (no other variables like attack cost/weakness/coin flips).
* The first Pokémon to 0 HP loses.

## Installation

```
cd tcgbattle
pip install -r requirements.txt
```

For config:

```
cp config.example.py config.py
# enter your config data in config.py
```
* Pokémon TCG API key from https://dev.pokemontcg.io/
* Create a Slack app and get a bot token with scopes `channels:join` and `chat:write` following the steps in https://api.slack.com/authentication/basics

## Usage

```
python tcgbattle.py [-h] {info,battle} ...

positional arguments:
  {info,battle}
    info         Shows info on a given Pokémon in the terminal from the Pokémon TCG Developers API
    battle       Battles two given Pokémon, and sends the results to Slack
```

Available Pokémon: https://pokemontcg.guru/set/base/base1

`'alakazam', 'blastoise', 'chansey', 'charizard', 'clefairy', 'gyarados', 'hitmonchan', 'machamp', 'magneton', 'mewtwo', 'nidoking', 'ninetales', 'poliwrath', 'raichu', 'venusaur', 'zapdos', 'beedrill', 'dragonair', 'dugtrio', 'electabuzz', 'electrode', 'pidgeotto', 'arcanine', 'charmeleon', 'dewgong', 'dratini', 'farfetchd', 'growlithe', 'haunter', 'ivysaur', 'jynx', 'kadabra', 'kakuna', 'machoke', 'magikarp', 'magmar', 'nidorino', 'poliwhirl', 'porygon', 'raticate', 'seel', 'wartortle', 'abra', 'bulbasaur', 'caterpie', 'charmander', 'diglett', 'doduo', 'drowzee', 'gastly', 'koffing', 'machop', 'magnemite', 'metapod', 'nidoran', 'onix', 'pidgey', 'pikachu', 'poliwag', 'ponyta', 'rattata', 'sandshrew', 'squirtle', 'starmie', 'staryu', 'tangela', 'voltorb', 'vulpix', 'weedle'`

## Credits

* Data from [Pokémon TCG Developers API](https://dev.pokemontcg.io/)
* Small sprites for battle start/end from [PokéSprite](https://github.com/msikma/pokesprite)
