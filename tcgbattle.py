#!/usr/bin/env python3

import argparse
import random
from pokemon import Pokemon
from pokemontcgapi import PokemonTCGAPI
from config import SlackConfig
from slack import SlackMessageBuilder
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

tcg_api = PokemonTCGAPI()
VALID_CARDS = []

slack_client = WebClient(token=SlackConfig.get("bot_token"))
slack_builder = SlackMessageBuilder(SlackConfig.get("channel"))

""" 
Get all Pokémon TCG set cards that are valid for battle.
Valid means in the Base 1 set, and card type is Pokémon (not other cards like items/trainers/etc.)
"""
def get_valid_cards():
    base1_cards = tcg_api.get()
    for card in base1_cards.get("data"):
        current_name = card.get("name").lower()

        # making edge cases (nidoran/farfetch'd) more easily usable from command line
        if current_name == "nidoran ♂": 
            current_name = "nidoran"
        elif current_name == "farfetch\'d":
            current_name = "farfetchd"

        VALID_CARDS.append(current_name)

def post_slack_block(message):
    slack_client.chat_postMessage(**message)

"""
Runs a battle between the two given Pokémon from start to end, and outputs the battle info to Slack.
"""
def battle_mons(mon1: Pokemon, mon2: Pokemon):
    message = slack_builder.battle_start_payload(mon1.name, mon2.name)
    post_slack_block(message)

    turn = 0
    while mon1.hpRemaining > 0 and mon2.hpRemaining > 0:
        turn += 1
        message = slack_builder.turn_payload(turn, mon1, mon2)
        post_slack_block(message)

        # mon1 attacks first, then they alternate
        if turn % 2 == 1:
            attack(mon1, mon2)
        else: 
            attack(mon2, mon1)
    end_battle(mon1, mon2)

"""
Takes 2 Pokémon, an attacker and a defender, and calculates damage to the defender based on one of the attacker's available attacks chosen at random.
If the card calls for damage based on certain conditions (e.g. flip a coin twice and do X damage for the number of heads), 
those conditions are ignored and it will just do straight damage for the base damage value of the attack.
"""
def attack(attacker: Pokemon, defender: Pokemon):
    current_attack = choose_attack(attacker)
    attack_name = current_attack.get("name")
    damage = current_attack.get("damage")
    
    # prevent negative HP
    if damage > defender.hpRemaining:
        defender.hpRemaining = 0
    else:
        defender.hpRemaining -= damage

    message = slack_builder.attack_payload(attacker, defender, attack_name, damage)
    post_slack_block(message)

"""
Chooses one of the given Pokémon's attacks at random.
"""
def choose_attack(attacker: Pokemon):
    random_attack_index = random.randint(0, len(attacker.attacks) - 1)
    return attacker.attacks[random_attack_index]

"""
Posts the winner of the battle in Slack.
"""
def end_battle(mon1: Pokemon, mon2: Pokemon):
    winner = mon1 if mon1.hpRemaining > 0 else mon2
    message = slack_builder.winner_payload(winner)
    post_slack_block(message)


if __name__ == "__main__":
    # Get the list of Base 1 cards for CLI to take as valid arguments. 
    # If the user gives an invalid Pokémon name, we can print a list of valid ones.
    get_valid_cards()

    # CLI stuff begins
    parser = argparse.ArgumentParser(prog="tcgbattle",
                                    description="Show info on or battle two Pokémon from the Pokémon TCG Base 1 set")

    subparsers = parser.add_subparsers(dest="command")
    info_parser = subparsers.add_parser("info", help="Shows info on a given Pokémon in the terminal from the Pokémon TCG Developers API")
    battle_parser = subparsers.add_parser("battle", help="Battles two given Pokémon, and sends the results to Slack")

    info_parser.add_argument("mon", type=str.lower, choices=VALID_CARDS)
    battle_parser.add_argument("mon1", type=str.lower, choices=VALID_CARDS)
    battle_parser.add_argument("mon2", type=str.lower, choices=VALID_CARDS)

    args = parser.parse_args()

    if args.command == "info": # Print information from the API about the selected Pokémon in the terminal
        print(tcg_api.get(args.mon))
        # mon = Pokemon(args.mon, tcg_api)
        # print(mon)
    elif args.command == "battle": # Begin a Pokémon battle with the given Pokémon
        mon1 = Pokemon(args.mon1, tcg_api)
        mon2 = Pokemon(args.mon2, tcg_api)
        print("Battle in progress, see Slack for output")
        battle_mons(mon1, mon2)