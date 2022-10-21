import requests
import json
import logs
import pokemonDatabase
import pokemonCard


class DownloadData:
    def __init__(self):
        self.downloadDataLogs = logs.Logger()
        self.URL = "https://pokeapi.co/api/v2/pokemon/?offset=0&limit=151"
        self.complete = False

    def download(self):
        try:
            content = requests.get(self.URL)
            parsedJson = json.loads(content.text)
            pokemonTuples = []
            for pokemon in parsedJson["results"]:
                pokemonTuples.append((pokemon["name"], pokemon["url"]))

            pokemonInfoList = []
            for pokemon in pokemonTuples:
                pokemonData = requests.get(pokemon[1])
                parsedPokemon = json.loads(pokemonData.text)
                tempPokemon = pokemonCard.Pokemon()
                tempPokemon.name = parsedPokemon["name"].capitalize()
                tempPokemon.artwork = parsedPokemon["sprites"]["other"]["official-artwork"]["front_default"]
                tempPokemon.attack = parsedPokemon["stats"][1]["base_stat"]
                tempPokemon.defence = parsedPokemon["stats"][2]["base_stat"]
                tempPokemon.type1 = parsedPokemon["types"][0]["type"]["name"].capitalize()
                if len(parsedPokemon["types"]) == 2:
                    tempPokemon.type2 = parsedPokemon["types"][1]["type"]["name"].capitalize()
                pokemonInfoList.append(tempPokemon)
            if len(pokemonInfoList) != 0:
                pokemonDatabase.addPokemonToDatabase(pokemonInfoList)
                self.complete = True
                self.downloadDataLogs.logger.info(f"List of {len(pokemonInfoList)} pokemon sucessfully added database.")
            else:
                self.complete = True
                self.downloadDataLogs.logger.info("No pokemon downloaded.")
        except Exception as e:
            self.downloadDataLogs.logger.error(e)
