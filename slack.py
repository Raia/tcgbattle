from pokemon import Pokemon

class SlackMessageBuilder:
	DIVIDER_BLOCK = {"type": "divider"}

	def __init__(self, channel):
		self.channel = channel
		self.username = "tcgbattlebot"

	def battle_start_payload(self, mon1_name: str, mon2_name: str):
		return {
		"channel": self.channel,
		"username": self.username,
		"text": "The battle has begun!",
		"blocks": [
			self.DIVIDER_BLOCK,
			self._get_intro_block(self, mon1_name, mon2_name),
			self.DIVIDER_BLOCK
		]
	}

	def turn_payload(self, turn: int, mon1: Pokemon, mon2: Pokemon):
		return {
			"channel": self.channel,
			"username": self.username,
			"text": "A new battle turn has begun.",
			"blocks": [
				self._get_turn_block(turn, mon1, mon2)
			]
		}

	def attack_payload(self, attacker: Pokemon, defender: Pokemon, attack_name: str, damage: int):
		return {
			"channel": self.channel,
			"username": self.username,
			"text": "Damage calculations...",
			"blocks": [
				self._get_attacker_block(attacker, attack_name),
				self._get_defender_block(defender, damage),
				self.DIVIDER_BLOCK
			]
		}
	
	def winner_payload(self, winner: Pokemon):
		return {
			"channel": self.channel,
			"username": self.username,
			"text": "The battle has ended!",
			"blocks": [
				self._get_winner_block(self, winner),
			]
		}

	
	@staticmethod
	def _get_turn_block(turn: int, mon1: Pokemon, mon2: Pokemon):
		text = f"*Turn {turn}* - {mon1.name}: {mon1.hpRemaining} HP, {mon2.name}: {mon2.hpRemaining} HP"
		return {"type": "section", "text": {"type": "mrkdwn", "text": text}}

	@staticmethod
	def _get_pokemon_sprite(pokemon: str):
		pokemon = pokemon.lower()

		# handling names with special characters
		# the card set only contains nidoran-m and not nidoran-f, so we set it to nidoran-m
		if pokemon == "nidoran ♂":
			pokemon = "nidoran-m"
		elif pokemon == "farfetch'd":
			pokemon = "farfetchd"
		
		return {"type": "image", 
				"image_url": f"https://github.com/msikma/pokesprite/blob/master/icons/pokemon/regular/{pokemon}.png?raw=true",
				"alt_text": pokemon
			}

	@staticmethod
	def _get_intro_block(self, mon1_name: str, mon2_name: str):
		mon1_sprite = self._get_pokemon_sprite(mon1_name)
		mon2_sprite = self._get_pokemon_sprite(mon2_name)

		text = f"A battle has begun between {mon1_name} and {mon2_name}!"

		return {"type": "context", "elements": [mon1_sprite, mon2_sprite, {"type": "mrkdwn", "text": text}]}
	
	@staticmethod
	def _get_attacker_block(attacker: Pokemon, attack_name: str):
		text = f"{attacker.name} used {attack_name}!"
		image_url = attacker.image_url

		return {"type": "section", 
				"text": {"type": "mrkdwn", "text": text}, 
				"accessory": {"type": "image","image_url": image_url, "alt_text": attacker.name}}

	@staticmethod
	def _get_defender_block(defender: Pokemon, damage: int):
		text = f"{defender.name} took {damage} damage and has {defender.hpRemaining} HP left!"
		image_url = defender.image_url

		return {"type": "section", 
				"text": {"type": "mrkdwn", "text": text}, 
				"accessory": {"type": "image","image_url": image_url, "alt_text": defender.name}}

	@staticmethod
	def _get_winner_block(self, winner: Pokemon):
		winner_sprite = self._get_pokemon_sprite(winner.name)
		text = f"The battle has ended. {winner.name} wins! :trophy:"
		return {"type": "context", "elements": [winner_sprite, {"type":"mrkdwn", "text": text}]}