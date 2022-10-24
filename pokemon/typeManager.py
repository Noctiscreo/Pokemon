from pokemon.pokemonCard import Pokemon


class TypesManager:
    # Singleton

    def downloadAndStore(self):
        pass

    def getDamagerMultiplier(self, attackType: str, defenderPokemon: Pokemon) -> float:
        return 1.0
