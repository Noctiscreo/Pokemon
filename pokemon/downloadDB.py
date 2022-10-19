import requests
import json
import logs
import pokemonDatabase

def downloadPokemonData() -> bool:
    downloadPokemonDataLogs = logs.Logger()
    POKEMONLIST_URL = "https://pokeapi.co/api/v2/pokemon/?offset=0&limit=151"

    try:
        content = requests.get(POKEMONLIST_URL)
        parsedJson = json.loads(content.text)
        pokemonTuples = []
        for pokemon in parsedJson["results"]:
            pokemonTuples.append((pokemon["name"], pokemon["url"]))

        pokemonInfoList = []
        for pokemon in pokemonTuples:
            pokemonDict = {}
            pokemonURL = pokemon[1]
            pokemonData = requests.get(pokemonURL)
            parsedPokemon = json.loads(pokemonData.text)
            pokemonDict["Name"] = parsedPokemon["name"].capitalize()
            pokemonDict["Artwork"] = parsedPokemon["sprites"]["front_default"]
            pokemonDict["Attack"] = parsedPokemon["stats"][1]["base_stat"]
            pokemonDict["Defence"] = parsedPokemon["stats"][2]["base_stat"]
            pokemonDict["Type1"] = parsedPokemon["types"][0]["type"]["name"].capitalize()
            if len(parsedPokemon["types"]) == 2:
                pokemonDict["Type2"] = parsedPokemon["types"][1]["type"]["name"].capitalize()
            else:
                pokemonDict["type2"] = None
            pokemonInfoList.append(pokemonDict)
        
        pokemonDatabase.addPokemonToDatabase(pokemonInfoList)
        downloadPokemonDataLogs.logger.info("List of pokemon sucessfully created and sent to database.")
        return True
    
    except:
        downloadPokemonDataLogs.logger.error("There was a problem downloading and creating the list of pokemon and sending to database.")
        return False
