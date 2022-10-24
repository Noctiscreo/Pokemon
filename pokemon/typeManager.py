from pokemon.pokemonCard import Pokemon
import logs
import requests
import json


class TypesManager:
    _instance = None

    def __init__(self):
        self.typesManagerLogs = logs.Logger()
        self.URL = "https://pokeapi.co/api/v2/type/"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TypesManager, cls).__new__(cls)
        return cls._instance

    def downloadAndStore(self):
        try:
            content = requests.get(self.URL)
            parsedJson = json.loads(content.text)
        except Exception as e:
            self.typesManagerLogs.logger.error(e)

    def getDamagerMultiplier(self, attackType: str, defenderPokemon: Pokemon) -> float:
        return 1.0
