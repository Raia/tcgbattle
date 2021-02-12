import re
from pokemontcgapi import PokemonTCGAPI

class Pokemon(object):
	def __init__(self, name: str, api: PokemonTCGAPI):
		self.name = name
		self.hpMax = self.hpRemaining = self.attacks = self.image_url = None
		self.api = api
		self.__set_info()
	
	def __set_info(self):
		card_data = self.api.get(self.name).get("data")
		card_data = self.__validate(card_data)

		self.name = card_data.get("name")
		self.hpMax = int(card_data.get("hp"))
		self.image_url = card_data.get("images").get("small")
		self.hpRemaining = self.hpMax
		self.attacks = self.__set_attacks(card_data.get("attacks"))
	
	def __set_attacks(self, attack_data: list):
		attacks = []
		for attack in attack_data:
			attack_name = attack.get("name")
			attack_damage = attack.get("damage") if attack.get("damage") else "0"

			# strip extra modifiers (coin flip, etc.) by removing anything that isn"t a digit
			attack_damage = int(re.sub(r"\D+", "", attack_damage))
			attacks.append({"name": attack_name, "damage": attack_damage})
		return attacks

	def __str__(self):
		return f"{self.name}: Attacks: {self.attacks}, Max HP: {self.hpMax}, HP remaining: {self.hpRemaining}, Image URL: {self.image_url}"
	
	# API response contains a "data" key mapped to a list, which is empty if no results were found for the search query.
	# If there was a result, we want the first element of the list. Otherwise, we raise an exception.
	def __validate(self, card_data):
		if not card_data:
			raise Exception(f"The Pokémon '{self.name}' could not be found. Please try again.")
		else:
			return card_data[0]