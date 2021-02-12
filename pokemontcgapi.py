import json
import requests
import backoff
from requests.exceptions import HTTPError
from config import TcgApiConfig

class PokemonTCGAPI:
    def __init__(self):
        self.url = TcgApiConfig.get("api_base_url")
        self.token = TcgApiConfig.get("api_key")
        
    """
    Gets all cards for Pokémon in set base1 if no Pokémon name is specified. 
    Otherwise, gets the card for the specified Pokémon.
    """
    @backoff.on_exception(backoff.expo,
                      (requests.exceptions.Timeout, requests.exceptions.ConnectionError),
                       max_tries=3)
    def get(self, name=None):
        query = "supertype:pokemon set.id:base1"
        if name:
            # edge case name that was modified to be more usable in CLI: slice off last character here otherwise it won't return result
            if name == "farfetchd":
                name = name[:-1]
            query += f" name:{name}"
        try:
            response = requests.get(self.url, params={"q": query})

            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Other error occurred: {err}")
        else:
            return(response.json())